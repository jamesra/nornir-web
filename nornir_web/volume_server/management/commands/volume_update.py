import os

from django.core.management.base import BaseCommand, CommandError

import nornir_djangomodel.import_xml as import_xml
from nornir_shared.argparse_helpers import NumberList
import nornir_web.volume_server.models as models


class Command(BaseCommand):
    args = '<volume_path ...>'
    help = 'Update the volume at the specified path' 

    def handle(self, *args, **options):

        coord_space_names = models.Mapping2D.objects.values('dest_coordinate_space').distinct()
        
        for coord_space in coord_space_names:
            db_coord_space = models.CoordSpace.objects.get(name=coord_space['dest_coordinate_space']) 
            
            if db_coord_space.UpdateAllBoundaries():
                print("Updated coord space %s " % db_coord_space.name)
            
            
            
        
