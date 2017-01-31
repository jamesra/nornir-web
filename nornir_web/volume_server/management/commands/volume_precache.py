from optparse import make_option
import os

from django.core.management.base import BaseCommand, CommandError 
from nornir_imageregistration import core
from nornir_imageregistration.spatial import *

import nornir_djangomodel.import_xml as import_xml
from nornir_shared.argparse_helpers import NumberList
from nornir_web.volume_server.models import AssembleSectionImage, CoordSpace, GetTilePaths, SaveTileGrid

from ...settings import VOLUME_SERVER_COORD_SPACE_RESOLUTION, VOLUME_SERVER_TILE_WIDTH, VOLUME_SERVER_TILE_HEIGHT


class Command(BaseCommand):
    '''Precache tiles for the specified sections and downsample levels'''
    
    args = '<sections downsample...>'
    help = 'Import or update the volume at the specified path'
    
    option_list = BaseCommand.option_list + (
                  make_option('--channel', dest='channel', default='TEM', type=str),
                  make_option('--filter', dest='filter', default='Leveled', type=str),
                  make_option('--sections', dest='sections', default=None, type=str),
                  make_option('--levels', dest='levels', default=None, type=str),
                  make_option('--coordspace', dest='coordspace', default='Grid', type=str)
                  )
               
    def handle(self, *args, **options):
          
        section_list = None
        if 'sections' in options:
            if not options['sections'] is None:
                section_list = NumberList(options['sections'])
            # if len(args) == 2:
            # section_list = NumberList(args[1])
            print("Importing only sections: %s" % str(section_list))
            
        downsample_list = None
        if 'levels' in options:
            if not options['levels'] is None:
                downsample_list = NumberList(options['levels'])
            # if len(args) == 2:
            # section_list = NumberList(args[1])
            print("Building downsample levels: %s" % str(downsample_list))            
        coord_space_name = options['coordspace']
        
        channel_name = 'TEM'
        if 'channel' in options:
            channel_name = options['channel']
            
        filter_name = 'Leveled'
        if 'filter' in options:
            filter_name = options['filter']
                
        
     
        if section_list is None:
            # Get the full image of the section at that downsample level
            coord_space = CoordSpace.objects.get(name=coord_space_name)
            if coord_space is None:
                raise ValueError("No coordinate space with name %s" % (coord_space_name))
            
            region = coord_space.GetBounds()
            section_list = range(int(region[iBox.MinZ]), int(region[iBox.MaxZ]) + 1)
          
        for section_number in section_list:
            tile_builder = TileBuilder(coord_space_name, section_number, channel_name, filter_name)
            tile_builder.BuildTilesForLevels(downsample_list)
            
        print('Successfully built tiles')
        
class TileBuilder(object):
    
    @property
    def FullImageName(self):
        return 'FullImage.png'
     
    def __init__(self, coord_space_name, section_number, channel_name, filter_name):
        
        self.section_number = section_number
        self.channel_name = channel_name
        self.filter_name = filter_name
        self.coord_space_name = coord_space_name
        
    def GetTilePaths(self, downsample_level):
        coord_space = CoordSpace.objects.get(name=self.coord_space_name)
        
        (tile_path, url_path) = GetTilePaths(coord_space.dataset.name,
                                             coord_space_name=coord_space.name,
                                             section_number=self.section_number,
                                             channel_name=self.channel_name,
                                             downsample=downsample_level)
        if not os.path.exists(tile_path):
            os.makedirs(tile_path)
            
        return tile_path
        
    def CarryImageToNextDownsampleLevel(self, input_image, input_downsample_level, output_downsample_level):
        
        print('Section #%d: Copy image from level %d to %d' % (self.section_number, input_downsample_level, output_downsample_level))
        
        tile_path = self.GetTilePaths(output_downsample_level)
        if not os.path.exists(tile_path):
            os.makedirs(tile_path)
            
        output_image = core.ResizeImage(input_image, input_downsample_level / output_downsample_level)
        
        output_image_full_path = os.path.join(tile_path, self.FullImageName)
        
        core.SaveImage(output_image_full_path, output_image)
        
    
    def BuildImageForLevel(self, downsample_level):
        
        print('Section #%d: Build image for level %d' % (self.section_number, downsample_level))
        
        coord_space = CoordSpace.objects.get(name=self.coord_space_name)
        resolution = VOLUME_SERVER_COORD_SPACE_RESOLUTION * downsample_level
         
        section_image = AssembleSectionImage(coord_space, self.section_number, resolution, channel_name=self.channel_name, filter_name=self.filter_name)
        if section_image is None:
            print('Could not generate image for section #%d' % (self.section_number))
            return None
        
        return section_image 
        # core.SaveImage(full_image_path, section_image) 
        
    def BuildTilesForLevels(self, downsample_levels):
        
        downsample_levels.sort()
        
        for iLevel, level in enumerate(downsample_levels):
            section_image = self.BuildTilesForLevel(level)
            
            if section_image is None:
                continue
            
            if iLevel + 1 < len(downsample_levels):
                self.CarryImageToNextDownsampleLevel(section_image, level, downsample_levels[iLevel + 1])
            
            del section_image
        return
        
        
    def BuildTilesForLevel(self, downsample_level):
         
        tile_shape = [VOLUME_SERVER_TILE_HEIGHT, VOLUME_SERVER_TILE_WIDTH] 
        # Check for a marker file indicating we've built tiles 
    
        tile_path = self.GetTilePaths(downsample_level)
        if not os.path.exists(tile_path):
            os.makedirs(tile_path)
        
        full_image_path = os.path.join(tile_path, 'FullImage.png')
        
        if not os.path.exists(full_image_path): 
            section_image = self.BuildImageForLevel(downsample_level)
            if section_image is None:
                print('Section #%d: Unable to generate image for level %d' % (self.section_number, downsample_level))
        
                return
            
            core.SaveImage(full_image_path, section_image)
        else:
            section_image = core.LoadImage(full_image_path)

        print('Section #%d: Create tiles for level %d' % (self.section_number, downsample_level))
        # Cut apart the full image to create tiles
        tiles = core.ImageToTiles(section_image, tile_size=tile_shape)
        
        print('Section #%d: Save tiles for level %d' % (self.section_number, downsample_level)) 
        SaveTileGrid(tiles, tile_path)

        return section_image
