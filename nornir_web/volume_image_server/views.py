# Create your views here.
import os
import nornir_imageregistration.core
from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from volume_image_server.settings import VOLUME_IMAGE_SERVER_IMAGE_ROOT, VOLUME_IMAGE_SERVER_IMAGE_URL
from . import models
from nornir_volumecontroller import Volume


'''
Image server takes the following query parameters and returns images registered into the volume

:param str v: Volume name
:param str c: Channel name 
:param float x: Position
:param float y: Position
:param float z: Position
:param float width: Width in pixels, defaults to minumum X resolution
:param float height: Height in pixels, defauls to minimum Y resolution
:param float depth: Depth in pixels, defaults to minimum Z resolution
:param float res: Requested resolution in the volume units, defaults to nm/sec
'''

def index(request):

    context = RequestContext(request, {})
    return render(request, 'volume_image_server\index.html', context)

def image_form(request, volume_name):
    volume_controller = models.GetVolumeControllerByName(volume_name)
    context = RequestContext(request, {"volume_name" : volume_controller.Name,
                                       "bounds" : volume_controller.Bounds,
                                       "max_resolution" : volume_controller.GetHighestResolution().X,
                                       "channels" : volume_controller.Channels})
    return render(request, 'volume_image_server\imageform.html', context)

def get_image(request, volume_name, channel_name):
    volume_controller = models.GetVolumeControllerByName(volume_name)
    region = BoundsFromPost(request.POST)
    resolution = ResolutionFromPost(request.POST)
    
    data = volume_controller.GetData(region, resolution, [channel_name])
    image_hrefs = data_to_images(data)

    context = RequestContext(request, {"volume_name" : volume_controller.Name,
                                       "bounds" : region,
                                       "resolution" : resolution,
                                       "channel" : channel_name,
                                       "image_to_href" : image_hrefs})

    return render(request, 'volume_image_server\imageresults.html', context)


def data_to_images(data_array):
    '''Temp function to save a data array to a file so it can be viewed in a template''' 

    image_map = {}
    for i, img in enumerate(data_array):
        image_name = ('%s_%d' % (img,i)) + '.png'
        data = data_array[img]
        image_path = os.path.join(VOLUME_IMAGE_SERVER_IMAGE_ROOT, image_name)
        href_path = os.path.join(VOLUME_IMAGE_SERVER_IMAGE_URL, image_name)

        nornir_imageregistration.core.SaveImage(image_path, data)

        image_map[image_name] = href_path

    return image_map


def ResolutionFromPost(post):
    return float(post["Resolution"])

def BoundsFromPost(post):
    bounds = [float(post["MinZ"]),
              float(post["MinY"]),
              float(post["MinX"]),
              float(post["MaxZ"]),
              float(post["MaxY"]),
              float(post["MaxX"])]
    return bounds

class VolumeDetails(DetailView):

    model = Volume

    def get_context_data(self, **kwargs):
        context = super(VolumeDetails, self).get_context_data(**kwargs)
        return context