
'''
Created on May 22, 2013

@author: u0490822
'''

import logging
import os
import shutil
import django.test

from nornir_shared.misc import SetupLogging


class TestBase(django.test.TestCase):
    '''
    classdocs
    '''

    @property
    def classname(self):
        return str(self.__class__.__name__)

    @property
    def TestInputPath(self):
        if 'TESTINPUTPATH' in os.environ:
            TestInputDir = os.environ["TESTINPUTPATH"]
            self.assertTrue(os.path.exists(TestInputDir), "Test input directory specified by TESTINPUTPATH environment variable does not exist")
            return TestInputDir
        else:
            self.fail("TESTINPUTPATH environment variable should specfify input data directory")

        return None

    @property
    def TestOutputPath(self):
        if 'TESTOUTPUTPATH' in os.environ:
            TestOutputDir = os.environ["TESTOUTPUTPATH"]
            return os.path.join(TestOutputDir, self.classname)
        else:
            self.fail("TESTOUTPUTPATH environment variable should specfify input data directory")

        return None

    @property
    def TestLogPath(self):
        if 'TESTOUTPUTPATH' in os.environ:
            TestOutputDir = os.environ["TESTOUTPUTPATH"]
            return os.path.join(TestOutputDir, "Logs", self.classname)
        else:
            self.fail("TESTOUTPUTPATH environment variable should specfify input data directory")

        return None

    @property
    def TestHost(self):
        if 'TESTHOST' in os.environ:
            return os.environ["TESTHOST"]

        return None

    @property
    def TestOutputURL(self):
        if self.TestHost is None:
            return None

        return self.TestHost + "/" + self.classname

    def setUp(self):

        super(TestBase, self).setUp()


        self.TestDataPath = self.TestInputPath

        # Remove output of earlier tests
        if os.path.exists(self.TestOutputPath):
            shutil.rmtree(self.TestOutputPath)

        os.makedirs(self.TestOutputPath)

        SetupLogging(self.TestLogPath)
        self.Logger = logging.getLogger(self.classname)


class PlatformTest(TestBase):
    @property
    def VolumePath(self):
        raise Exception("VolumePath property not implemented")

    @property
    def Platform(self):
        raise Exception("Platform property not implemented")

    @property
    def PlatformFullPath(self):
        return os.path.join(self.TestDataPath, "PlatformRaw", self.Platform)

    @property
    def ImportedDataPath(self):
        if self.VolumePath and len(self.VolumePath) > 0:
            return os.path.join(self.PlatformFullPath, self.VolumePath)
        else:
            return self.PlatformFullPath
