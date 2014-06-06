from django.db import models
from volume_importer.settings import VOLUME_IMPORTER_VOLUME_DIRS

import nornir_volumecontroller as vc

import nornir_shared.files

# Create your models here.

def SearchFilesystemForVolumes(path):
    '''Recursively search the provided path until each directory containing a volume.xml file is found'''
    
    return nornir_shared.files.RecurseSubdirectoriesGenerator(path, RequiredFiles=["VolumeData.xml"])


def GetVolumeController(volume_path):
     try:
        volume_controller = vc.CreateVolumeController(volume_path) 
     except ValueError as e:
        return None
       
     return volume_controller


def GetVolumes():
    volume_paths = []
    for volume_dir in VOLUME_IMPORTER_VOLUME_DIRS:

        volume_paths.extend(list(SearchFilesystemForVolumes(volume_dir)))

    volume_controllers = []
    for volume_path in volume_paths:

        try:
            volume = GetVolumeController(volume_path)
            volume_controllers.append(volume)
        except ValueError as e:
            pass

    return volume_controllers