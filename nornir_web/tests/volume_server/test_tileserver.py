'''
Created on Jul 23, 2014

@author: u0490822
'''
from .. import  test_base
from django.test import Client

import volume_server.management.commands.volume_import as volume_import

import volume_server.viking_views as viking_views


class TestTileServer(test_base.PlatformTest):

    @property
    def VolumePath(self):
        return "IDocBuildTest"

    @property
    def Platform(self):
        return "IDoc"


    def setUp(self):
        importCommand = volume_import.Command()
        importCommand.handle(self.ImportedDataPath)
        return

    def tearDown(self):
        return

    def test_get_tile(self):
        c = Client()
        response = c.post('/volume_server/IDocBuildTest/691/TEM/8/T_X1_Y1.png')
        
        self.assertIsNotNone(response)

#        viking_views.get_tile(request, dataset_name=self.VolumePath, section_number=692, channel_name="TEM", downsample=16, column=1, row=1)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    import unittest
    unittest.main()