from django.core.management.base import BaseCommand, CommandError 
import nornir_djangomodel.import_xml as import_xml
from nornir_imageregistration import core
from nornir_imageregistration.spatial import *
from nornir_shared.argparse_helpers import NumberList
from optparse import make_option
import os


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
            section_list = NumberList(options['sections'])
            #if len(args) == 2:
            #section_list = NumberList(args[1])
            print("Importing only sections: %s" % str(section_list))
            
        downsample_list = None
        if 'levels' in options:
            downsample_list = NumberList(options['levels'])
            #if len(args) == 2:
            #section_list = NumberList(args[1])
            print("Building downsample levels: %s" % str(downsample_list))            
        coord_space_name = options['coordspace']
        
        channel_name = 'TEM'
        if 'channel' in options:
            channel_name = options['channel']
            
        filter_name = 'Leveled'
        if 'filter' in options:
            filter_name = options['filter']
                
        #Get the full image of the section at that downsample level
        coord_space = CoordSpace.objects.get(name=coord_space_name)
        if coord_space is None:
            raise ValueError("No coordinate space with name %s" % (coord_space_name))
     
        if section_list is None:
            region = coord_space.GetBounds()
            section_list = range(region[iBox.minZ], region[iBox.maxZ]+1)
        
        tile_shape = [VOLUME_SERVER_TILE_HEIGHT, VOLUME_SERVER_TILE_WIDTH]
        resolution = VOLUME_SERVER_COORD_SPACE_RESOLUTION * downsample_list[0]
        for section_number in section_list: 
            print('Assemble section #%d' % (section_number))
            #Check for a marker file indicating we've built tiles
        
            (tile_path, url_path) = GetTilePaths(coord_space.dataset.name, coord_space_name=coord_space_name, section_number=section_number, channel_name=channel_name, downsample=downsample_list[0])
            if not os.path.exists(tile_path):
                os.makedirs(tile_path)
            
            full_image_path = os.path.join(tile_path, 'FullImage.png')
            
            if not os.path.exists(full_image_path):
                section_image = AssembleSectionImage(coord_space, section_number, resolution, channel_name=channel_name, filter_name=filter_name)
                if section_image is None:
                    continue 
                
                core.SaveImage(full_image_path, section_image)
            else:
                section_image = core.LoadImage(full_image_path)
             
            print('Creating tiles for section #%d' % (section_number))
            #Cut apart the full image to create tiles
            tiles = core.ImageToTiles(section_image, tile_size=tile_shape)
            
                        
            print('Saving tiles for section #%d' % (section_number)) 
            SaveTileGrid(tiles, tile_path)
        
        print('Successfully built tiles')
        