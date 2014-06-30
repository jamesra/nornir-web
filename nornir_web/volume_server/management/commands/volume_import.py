from django.core.management.base import BaseCommand, CommandError
from nornir_djangomodel.models import *
import nornir_djangomodel.import_xml as import_xml
import os

class Command(BaseCommand):
    args = '<volume_path ...>'
    help = 'Import or update the volume at the specified path'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("import directory not specified")

        for volume_path in args:
            if not os.path.exists(volume_path):
                raise CommandError("Requested import directory does not exist:\n\t" + os.path.abspath(volume_path))

            volume_xml_path = os.path.join(volume_path, 'VolumeData.xml')
            if not os.path.exists(volume_path):
                raise CommandError("Requested import file does not exist:\n\t" + os.path.abspath(volume_xml_path))

            dataset_name = import_xml.VolumeXMLImporter.Import(volume_xml_path)

            self.stdout.write('Successfully imported dataset %s from %s' % (dataset_name, volume_path))