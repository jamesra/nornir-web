from django.db import models
from volume_image_server.settings import VOLUME_IMAGE_SERVER_VOLUME_DIRS

import nornir_volumecontroller as vc
import os

import nornir_shared.files

# Create your models here.

_volume_controllers = {}

def SearchFilesystemForVolumes(path):
    '''Recursively search the provided path until each directory containing a volume.xml file is found'''
    
    return nornir_shared.files.RecurseSubdirectoriesGenerator(path, RequiredFiles=["VolumeData.xml"])


def GetVolumeControllerByName(volume_name):
    if volume_name in _volume_controllers:
        return _volume_controllers[volume_name]

    volume_full_path = GetVolumeFullPath(volume_name)
    if not os.path.exists(volume_full_path):
        return None

    volume_controller = GetVolumeController(volume_full_path)
    _volume_controllers[volume_name] = volume_controller
    return volume_controller

def GetVolumeFullPath(volume_path_name):
    for volume_dir in VOLUME_IMAGE_SERVER_VOLUME_DIRS:
        volume_full_path = os.path.join(volume_dir, volume_path_name, "VolumeData.xml")
        if os.path.exists(volume_full_path):
            return volume_full_path

    return None

def GetVolumeController(volume_full_path):
    try:
        volume_controller = vc.CreateVolumeController(volume_full_path) 
    except ValueError as e:
        return None
       
    return volume_controller

def GetVolumes():
    volume_paths = []
    for volume_dir in VOLUME_IMAGE_SERVER_VOLUME_DIRS:

        volume_paths.extend(list(SearchFilesystemForVolumes(volume_dir)))

    volume_controllers = []
    for volume_path in volume_paths:

        try:
            volume = GetVolumeController(volume_path)
            volume_controllers.append(volume)
        except ValueError as e:
            pass

    return volume_controllers