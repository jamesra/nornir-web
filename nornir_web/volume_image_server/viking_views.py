# Create your views here.
import os
import mimetypes

import nornir_imageregistration.core
from django.template import RequestContext
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.views.generic.detail import DetailView
from volume_image_server.settings import VOLUME_IMAGE_SERVER_TILE_CACHE_ROOT, VOLUME_IMAGE_SERVER_TILE_CACHE_URL, VOLUME_IMAGE_SERVER_TILE_WIDTH, VOLUME_IMAGE_SERVER_TILE_HEIGHT, VOLUME_IMAGE_SERVER_TILE_CACHE_ENABLED
from . import models
from nornir_volumecontroller import Volume


def get_tile(request, volume_name, section_number, channel_name, downsample, column, row):
    if not isinstance(section_number, int):
        section_number = int(section_number)
    if not isinstance(downsample, float):
        downsample = float(downsample)
    if not isinstance(column, int):
        column = int(column)
    if not isinstance(row, int):
        row = int(row)

    (file_path, url_path) = GetTileFilename(volume_name, section_number, channel_name, downsample, column, row)
    if VOLUME_IMAGE_SERVER_TILE_CACHE_ENABLED and os.path.exists(file_path):
        return SendImageResponse(request, file_path, url_path)

    volume_controller = models.GetVolumeControllerByName(volume_name)
    region = BoundsForTile(section_number, downsample, column, row)
    
    resolution = volume_controller.GetHighestResolution(channel_names=[channel_name]).X * downsample
    
    #TODO: if os.path.exists(file_path): return file_path

    data = volume_controller.GetData(region, resolution, [channel_name])
    data_to_images(data[section_number], file_path)
    return SendImageResponse(request, file_path, url_path)

    
def SendImageResponse(request, file_path, url_path):
    with open(file_path, "rb") as f:
        try:
            png_data = f.read()
            return HttpResponse(png_data, mimetype=mimetypes.guess_type(file_path)[0])

        except Exception as e:
            return page_not_found(request, template_name='500.html')  

def BoundsForTile(section_number, downsample, column, row):
    
    tile_width = VOLUME_IMAGE_SERVER_TILE_WIDTH * downsample
    tile_height = VOLUME_IMAGE_SERVER_TILE_HEIGHT * downsample

    start_y = tile_height * row
    start_x = tile_width * column

    bounds = [float(section_number),
              float(start_y),
              float(start_x),
              float(float(section_number)),
              float(start_y + tile_height),
              float(start_x + tile_width)]
    return bounds


def GetTileFilename(volume_name, section_number, channel_name, downsample, column, row):
    sub_path = os.path.join(volume_name, '%04d' % (section_number), channel_name, '%03d' % (int(downsample)), 'X%03d_Y%03d.png' % (column, row))
    file_path = os.path.join(VOLUME_IMAGE_SERVER_TILE_CACHE_ROOT, sub_path)
    url_path = os.path.join(VOLUME_IMAGE_SERVER_TILE_CACHE_URL, sub_path)
    return (file_path, url_path)


def data_to_images(image, image_path):
    '''Temp function to save a data array to a file so it can be viewed in a template''' 

    dir_path = os.path.dirname(image_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
         
    nornir_imageregistration.core.SaveImage(image_path, image)
    return 
