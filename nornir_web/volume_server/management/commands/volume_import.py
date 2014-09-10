from django.core.management.base import BaseCommand, CommandError
from nornir_djangomodel.models import *
import nornir_djangomodel.import_xml as import_xml
from nornir_shared.argparse_helpers import NumberList
from optparse import make_option
import os

class Command(BaseCommand):
    args = '<volume sections ...>'
    help = 'Import or update the volume at the specified path'
    option_list = BaseCommand.option_list + ( 
                  make_option('--sections', dest='sections', default=None, type='str'),            
                                            )
     
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("import directory not specified")
        
        volume_path = args[0]

        section_list = None
        if 'sections' in options:
            if not options['sections'] is None:
                section_list = NumberList(options['sections'])
                #if len(args) == 2:
                #section_list = NumberList(args[1])
                print("Importing only sections: %s" % str(section_list))

        if not os.path.exists(volume_path):
            raise CommandError("Requested import directory does not exist:\n\t" + os.path.abspath(volume_path))
        
        volume_xml_path = os.path.join(volume_path, 'VolumeData.xml')
        if not os.path.exists(volume_path):
            raise CommandError("Requested import file does not exist:\n\t" + os.path.abspath(volume_xml_path))
        
        dataset_name = import_xml.VolumeXMLImporter.Import(volume_xml_path, section_list=section_list)
        
        print('Successfully imported dataset %s from %s' % (dataset_name, volume_path))