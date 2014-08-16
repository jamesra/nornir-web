# Create your views here.
import os
import mimetypes
import math

import nornir_imageregistration.core
import nornir_imageregistration.spatial as spatial
from django.template import RequestContext
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.views.generic.detail import DetailView
from django.views.defaults import page_not_found

import cProfile
import numpy
 
from nornir_web.volume_server.settings import VOLUME_SERVER_COORD_SPACE_RESOLUTION
from nornir_web.volume_server.settings import VOLUME_SERVER_COORD_SPACE_PROFILE_ENABLED, VOLUME_SERVER_TILE_CACHE_ROOT, VOLUME_SERVER_TILE_CACHE_URL, VOLUME_SERVER_TILE_WIDTH, VOLUME_SERVER_TILE_HEIGHT, VOLUME_SERVER_TILE_CACHE_ENABLED

from . import  models
# from nornir_djangocontroller import Volume

def get_default_blank_tile_path(): 
    tile_name = "default_empty_%d_%d.png" % (VOLUME_SERVER_TILE_WIDTH, VOLUME_SERVER_TILE_HEIGHT)
    tile_path = os.path.join(VOLUME_SERVER_TILE_CACHE_ROOT, tile_name)
    url_path = os.path.join(VOLUME_SERVER_TILE_CACHE_URL, tile_name)
    return (tile_path, url_path)

def get_or_create_default_blank_tile():
    (tile_path, url_path) = get_default_blank_tile_path()
    if not os.path.exists(tile_path):
        empty_image = numpy.zeros((VOLUME_SERVER_TILE_HEIGHT, VOLUME_SERVER_TILE_WIDTH))
        nornir_imageregistration.core.SaveImage(tile_path, empty_image)
    
    return (tile_path, url_path)

(blank_file_path, blank_url_path) = get_or_create_default_blank_tile()


def get_tile(request, dataset_name, coord_space_name, section_number, channel_name, downsample, column, row):
  
    filter_name = 'Leveled'

    if not isinstance(section_number, int):
        section_number = int(section_number)
    if not isinstance(downsample, float):
        downsample = float(downsample)
    if not isinstance(column, int):
        column = int(column)
    if not isinstance(row, int):
        row = int(row)

    (file_path, url_path) = GetTileFullPaths(dataset_name, coord_space_name, section_number, channel_name, downsample, column, row)
    if VOLUME_SERVER_TILE_CACHE_ENABLED and os.path.exists(file_path):
        print("Cached response for %s" % file_path)
        return SendImageResponse(request, file_path, url_path, os.path.getsize(file_path))
    
    print("Generate tile %s" % file_path)
    if VOLUME_SERVER_COORD_SPACE_PROFILE_ENABLED:
        profiler = cProfile.Profile()
        profiler.enable(subcalls=True, builtins=True)

    coord_space = get_object_or_404(models.CoordSpace, name=coord_space_name)
    region = BoundsForTile(section_number, downsample, column, row)
     
    resolution = VOLUME_SERVER_COORD_SPACE_RESOLUTION * downsample

    try:
        data = models.GetData(coord_space, region, resolution, channel_name, filter_name)
    except models.NoDataInRegion:
        print("\tNo data in region: %s" % os.path.basename(file_path))
        return SendImageResponse(request, blank_file_path, blank_url_path, os.path.getsize(blank_file_path))
    except models.OutOfBounds:
        print("\tTile out of bounds: %s" % os.path.basename(file_path))
        return SendOutOfBoundsResponse(request, os.path.basename(file_path), TileBounds(coord_space.bounds.as_tuple(), downsample))
    
    if data is None:
        print("Unable to generate tile %s" % file_path)
        return page_not_found(request)
#
#   TODO: if os.path.exists(file_path): return file_path
#   data = volume_controller.GetData(region, resolution, [channel_name])
    data_to_images(data, file_path)

    if VOLUME_SERVER_COORD_SPACE_PROFILE_ENABLED:
        profiler.disable()
        profiler.dump_stats(file_path + ".profile")

    print("\tResponse sent for %s" % file_path)
    return SendImageResponse(request, file_path, url_path, os.path.getsize(file_path))



def TileBounds(boundary_rect, downsample):
    ''':return: (minY, minX, maxY, maxX) of tiles for the given downsample value'''
    
    (tile_height, tile_width) = GetTileSize(downsample)
     
    return (math.floor(boundary_rect[spatial.iBox.MinY] / tile_height),
            math.floor(boundary_rect[spatial.iBox.MinX] / tile_width),
            math.floor(boundary_rect[spatial.iBox.MaxY] / tile_height),
            math.floor(boundary_rect[spatial.iBox.MaxX] / tile_width))


def SendOutOfBoundsResponse(request, file_path, tileBounds): 
    context = {'file_path': file_path,
               'min_tile_x' : tileBounds[spatial.iRect.MinX],
               'min_tile_y' : tileBounds[spatial.iRect.MinY],
               'max_tile_x' : tileBounds[spatial.iRect.MaxX],
               'max_tile_y' : tileBounds[spatial.iRect.MaxY]}
    
    return render(request, 'volume_server/tile_out_of_bounds.html', context, status=404)


def SendImageResponse(request, file_path, url_path, response_size):
    with open(file_path, "rb") as f:
        try:
            png_data = f.read()
            response = HttpResponse(png_data, content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Length'] = response_size
            return response


        except Exception as e:
            return page_not_found(request, template_name='500.html')
        
def GetTileSize(downsample):
    ''':return: (width, height) of tiles in volume coordinates for given downsample level'''
    tile_width = VOLUME_SERVER_TILE_WIDTH * downsample
    tile_height = VOLUME_SERVER_TILE_HEIGHT * downsample
    
    return (tile_height, tile_width)

def BoundsForTile(section_number, downsample, column, row):

    (tile_height, tile_width) = GetTileSize(downsample)

    start_y = tile_height * row
    start_x = tile_width * column

    bounds = [float(section_number),
              float(start_y),
              float(start_x),
              float(float(section_number)),
              float(start_y + tile_height),
              float(start_x + tile_width)]
    return bounds


def data_to_images(image, image_path):
    '''Temp function to save a data array to a file so it can be viewed in a template'''

    dir_path = os.path.dirname(image_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    nornir_imageregistration.core.SaveImage(image_path, image)
    return
