'''
Created on Jul 23, 2014

@author: u0490822
'''
from .. import  test_base
from django.test import Client

import volume_server.management.commands.volume_import as volume_import
import volume_server.management.commands.volume_precache as volume_precache


class TestTileServer(test_base.PlatformTest):
    
    
    def assert_status_code(self,response, ExpectedCode=200):
        self.assertEqual(response.status_code, ExpectedCode, "Invalid status code %d, expected %d" % (response.status_code, ExpectedCode))        

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
#===============================================================================
# 
#     def test_get_tile(self):
#         c = Client()
#         
#         #Out of X,Y bounds
#         response = c.post('/volume_server/IDocBuildTest/Grid/691/TEM/8/T_X1000000_Y1000000.png')
#         self.assertIsNotNone(response)
#         self.assert_status_code(response, 404)
#         
#         #Out of Z bounds
#         response = c.post('/volume_server/IDocBuildTest/Grid/1/TEM/8/T_X1000000_Y1000000.png')
#         self.assertIsNotNone(response)
#         self.assert_status_code(response, 404)
#         
#         #Valid Tile
#         response = c.post('/volume_server/IDocBuildTest/Grid/691/TEM/8/T_X1_Y1.png')
#         self.assertIsNotNone(response)
#         self.assert_status_code(response, 200)
#         
#         #Valid Tile
#         response = c.post('/volume_server/IDocBuildTest/ChannelToVolume/691/TEM/8/T_X1_Y1.png')
#         self.assertIsNotNone(response)
#         self.assert_status_code(response, 200)
#===============================================================================
        
    def test_precache(self):
        
        precacheCommand = volume_precache.Command()
        precacheCommand.handle(sections='696', levels='16,32', coordspace='Grid')
        
        
        
        
         
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    import unittest
    unittest.main()