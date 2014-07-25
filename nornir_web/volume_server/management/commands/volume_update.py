from django.core.management.base import BaseCommand, CommandError
import nornir_web.volume_server.models as models
import nornir_djangomodel.import_xml as import_xml
from nornir_shared.argparse_helpers import NumberList
import os

class Command(BaseCommand):
    args = '<volume_path ...>'
    help = 'Update the volume at the specified path'

    def handle(self, *args, **options):

        for coord_space in models.CoordSpace.objects.all():
            if coord_space.UpdateAllBoundaries():
                print("Updated coord space %s " % coord_space.name) 
            
        