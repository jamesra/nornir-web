import operator
import nornir_djangomodel.models as models
import nornir_imageregistration.spatial as spatial
import nornir_imageregistration.transforms.utils
import numpy as np

class OutOfBounds(Exception):
    '''Indicates a request was out of the volume boundaries'''
    pass

class NoDataInRegion(Exception):
    pass

def DestinationBoundsFromMappings(mappings):
    '''Given a set of Mapping2D objects return the bounding box
    :return: ndarray [minZ, minY, minX, maxZ, maxY, maxX]'''

    points = None
    for mapping in mappings:
        bounding_box = Mapping2D.DestBoundingBox(mapping)
        if points is None:
            points = bounding_box.BottomLeftFront
        else:
            points = np.vstack((points, bounding_box.BottomLeftFront))

        points = np.vstack((points, bounding_box.TopRightBack))

    return spatial.BoundingBox.CreateFromPoints(points)

class BoundingBox(models.BoundingBox):

    class Meta:
        proxy = True

class Dataset(models.Dataset):

    class Meta:
        proxy = True

class Data2D(models.Data2D):

    class Meta:
        proxy = True

    @classmethod
    def HighestResolutionData(cls, Tiles):
        '''Return the row with the highest resolution from the list of Data2D objects'''

        if Tiles is None or len(Tiles) == 0:
            raise ValueError("Tiles argument is required to be a non-empty list.")

        Tiles = sorted(Tiles, key=operator.attrgetter('level'), reverse=True)
        return Tiles[0]

class Mapping2D(models.Mapping2D):

    @classmethod
    def DestBoundingBox(cls, mapping):
        return spatial.BoundingBox.CreateFromBounds(mapping.dest_bounding_box.as_tuple())

    @classmethod
    def SrcBoundingBox(cls, mapping):
        return spatial.BoundingBox.CreateFromBounds(mapping.src_bounding_box.as_tuple())

    @classmethod
    def GetTileByResolution(cls, mapping, db_filter, resolution):
        downsample_level = int((resolution / mapping.src_coordinate_space.scale_value_X))
        return cls.GetTileByDownsample(mapping, db_filter, downsample_level)
    
    @classmethod
    def GetTileByDownsample(cls, mapping, db_filter, downsample_level):
        Tiles = mapping.src_coordinate_space.data2d_set.filter(level__lte=downsample_level, filter=db_filter)
        
        #Tiles = Data2D.objects.filter(level__lte=downsample_level, coord_space=mapping.src_coordinate_space, filter=db_filter)
        if len(Tiles) == 0:
            return None

        Tile = Data2D.HighestResolutionData(Tiles)
        return Tile

    class Meta:
        proxy = True

class CoordSpace(models.CoordSpace):

    class Meta:
        proxy = True

    def GetBounds(self):
        if len(self.incoming_mappings.all()) is 0:
            return self.bounds

        bbox = DestinationBoundsFromMappings(self.incoming_mappings.all())
        # self.bounds = bbox
        # self.save()

        return bbox.ToArray()

    def MappingsWithinBounds(self, region):
        '''Return all mappings who map within the specified region
        :param region: [MinZ minY, minX, maxZ, maxY, maxX] or BoundingBox'''
        if not isinstance(region, spatial.BoundingBox):
            region = spatial.BoundingBox(region)

#         mappings = []
#         for mapping in self.incoming_mappings.select_related('dest_bounding_box').filter(dest_bounding_box__minZ__lte=region[spatial.iBox.MaxZ],
#                                                                                          dest_bounding_box__maxZ__gte=region[spatial.iBox.MinZ],
#                                                                                          dest_bounding_box__minX__lte=region[spatial.iBox.MaxX],
#                                                                                          dest_bounding_box__maxX__gte=region[spatial.iBox.MinX],
#                                                                                          dest_bounding_box__minY__lte=region[spatial.iBox.MaxY],
#                                                                                          dest_bounding_box__maxY__gte=region[spatial.iBox.MinY]):
#             dest_bbox = Mapping2D.DestBoundingBox(mapping)
#             if spatial.BoundingBox.contains(region, dest_bbox):
#                 mappings.append(mapping) 

        return self.incoming_mappings.filter(dest_bounding_box__minZ__lte=region[spatial.iBox.MaxZ],
                                                  dest_bounding_box__maxZ__gte=region[spatial.iBox.MinZ],
                                                  dest_bounding_box__minX__lte=region[spatial.iBox.MaxX],
                                                  dest_bounding_box__maxX__gte=region[spatial.iBox.MinX],
                                                  dest_bounding_box__minY__lte=region[spatial.iBox.MaxY],
                                                  dest_bounding_box__maxY__gte=region[spatial.iBox.MinY])

def GetMappings(coordspace, region):
    ''':return: None if no data in region, otherwise ndarray image'''
    assert(isinstance(region, spatial.BoundingBox))
    potential_mappings = coordspace.MappingsWithinBounds(region)
    if potential_mappings is None:
        raise NoDataInRegion()
    
    return potential_mappings


def GetData(coordspace, region, resolution, channel_name, filter_name):
    ''':return: None if no data in region, otherwise ndarray image'''
    if not isinstance(region, spatial.BoundingBox):
        region = spatial.BoundingBox(region)
        
    if not RegionWithinCoordSpace(region, coordspace):
        raise OutOfBounds()

    potential_mappings = GetMappings(coordspace, region) 
    
    
    db_channel = models.Channel.objects.get(name=channel_name, dataset=coordspace.dataset)
    db_filter = models.Filter.objects.get(name=filter_name, channel=db_channel)
    
    (image_to_transform, requiredScale) = MappingsToTiles(potential_mappings, db_filter, resolution=resolution)
    if len(image_to_transform) == 0:
        return None

    mosaic = nornir_imageregistration.mosaic.Mosaic(image_to_transform)

    (image, mask) = mosaic.AssembleTiles(tilesPath=coordspace.dataset.path, FixedRegion=region.RectangleXY.ToArray(), usecluster=True, requiredScale=requiredScale)

    return image


def RegionWithinCoordSpace(region, coord_space):
    #TODO, update the importer to update the coord_space bounding box when new Z levels are added 
    coord_space_bounds = coord_space.bounds.as_tuple() 
    coord_space_bounding_box = spatial.BoundingBox.CreateFromBounds(coord_space_bounds)
    if not spatial.BoundingBox.contains(region, coord_space_bounding_box):
        return False
    
    return True


def MappingsToTiles(mappings, db_filter, resolution=None, downsample=None):
    '''Grab the appropriate Data2D objects representing tiles used as input to the mappings
    :return: Tuple, (dict, scale) indicating paths to image tiles and the scale relative to the transforms'''
    
    #Resolution or downsample must be specified
    assert(not (resolution is None and downsample is None))
    image_to_transform = {}
    requiredScale = None

    for mapping in mappings:
        tile = None
        if resolution:
            tile = Mapping2D.GetTileByResolution(mapping, db_filter, resolution)
        else:
            tile = Mapping2D.GetTileByDownsample(mapping, db_filter, downsample)
            
        if tile is None:
            continue
        
        if requiredScale is None:
            requiredScale = tile.level
        else:
            assert(requiredScale == tile.level)

        transform = mapping.transform_string

        image_to_transform[tile.relative_path] = transform
        
    if requiredScale == None:
        return (image_to_transform, None)

    return (image_to_transform, 1.0 / requiredScale)










