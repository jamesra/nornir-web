import operator
import nornir_djangomodel.models as models
import nornir_imageregistration.spatial as spatial
import nornir_imageregistration.transforms.utils
import numpy as np

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
    def GetTile(cls, mapping, db_filter, resolution=None):
        downsample_level = int((resolution / mapping.src_coordinate_space.scale_value_X))

        Tiles = Data2D.objects.filter(level__lte=downsample_level, filter=db_filter, coord_space=mapping.src_coordinate_space)
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

        mappings = []
        for mapping in self.incoming_mappings.select_related('dest_bounding_box'):
            dest_bbox = Mapping2D.DestBoundingBox(mapping)
            if spatial.BoundingBox.contains(region, dest_bbox):
                mappings.append(mapping)

        return mappings


def GetData(coordspace, region, resolution, channel_name, filter_name):
    ''':return: None if no data in region, otherwise ndarray image'''
    if not isinstance(region, spatial.BoundingBox):
        region = spatial.BoundingBox(region)

    potential_mappings = coordspace.MappingsWithinBounds(region)
    if len(potential_mappings) == 0:
        return None

    db_channel = models.Channel.objects.get(name=channel_name, dataset=coordspace.dataset)
    # Grab the data2D rows for tiles at the correct levels
    db_filter = models.Filter.objects.get(name=filter_name, channel=db_channel)
    image_to_transform = MappingsToTiles(potential_mappings, db_filter, resolution)

    if len(image_to_transform) == 0:
        return None


    mosaic = nornir_imageregistration.mosaic.Mosaic(image_to_transform)

    (image, mask) = mosaic.AssembleTiles(tilesPath=coordspace.dataset.path, FixedRegion=region.RectangleXY.ToArray(), usecluster=False)

    return image

    # Create a mosaic to pass to assemble

    # Return the generated image


def MappingsToTiles(mappings, db_filter, resolution=None):
    '''Grab the appropriate Data2D objects representing tiles used as input to the mappings'''
    image_to_transform = {}

    for mapping in mappings:
        tile = Mapping2D.GetTile(mapping, db_filter, resolution)
        if tile is None:
            continue

        transform = mapping.transform_string

        image_to_transform[tile.relative_path] = transform

    return image_to_transform










