import test.test_base
import os
from django.core.management import call_command
import nornir_djangomodel.import_xml as import_xml

import nornir_djangomodel.models as models


class ImportVolumeXMLTestCase(test.test_base.PlatformTest):

    @property
    def VolumePath(self):
        return "IDocBuildTest"

    @property
    def Platform(self):
        return "IDOC"

    def setUp(self):
        super(ImportVolumeXMLTestCase, self).setUp()

        call_command('syncdb')

        self.VolumeXMLFullPath = os.path.join(self.ImportedDataPath, 'VolumeData.xml')

    def test_import_volumexml(self):
        import_xml.Import(self.VolumeXMLFullPath)

        # Print the volumes in the DB
        vlist = models.Volume.objects.all()
        self.assertEqual(len(vlist), 1, "Only one volume expected")
        self.assertEqual(vlist[0].path, self.ImportedDataPath)

        clist = models.Channel.objects.all()
        print("\nChannels:")
        for c in clist:
            print(c.name)

        flist = models.Filter.objects.all()
        print("\nFilters:")
        for f in flist:
            print(f.name)

        # Check that the volume was imported
        print("\nData 2D:")
        for i in models.Data2D.objects.all():
            print(i.coord_space.name + '  ' + i.relative_path)

        # Check that the volume was imported
        print("\nTiles:")
        for t in models.Tile.objects.all():
            print(t.name + ' ' + t.coord_space.name)

        # Check that the volume was imported
        print("\nCoordSpace:")
        for c in models.CoordSpace.objects.all():
            print(c.name + " " + str(c.bounds))

        print("\Mappings:")
        for m in models.Tile2DMapping.objects.all():
            print(m.tile.coord_space.name + " -> " + m.dest_coordinate_space.name)

        c = models.CoordSpace.objects.get(name='695.TEM.ChannelToVolume')
        print(c.name)
