
import nornir_djangomodel.models as models

class VolumeInterface(object):

    @property
    def Bounds(self):
        '''Bounding box of the entire volume'''
        raise NotImplemented("Abstract base class")

    @property
    def Channels(self):
        '''List of all channels available in the volume'''
        raise NotImplemented("Abstract base class")

    def GetData(self, region, resolution, channels):
        '''Get the raw data inside the boundaries
        :param box region: Data within the region is returned
        :param ndarray resolution: The resolution to return data in
        :param list channels: List of channels to assign to the output array
        :returns: 4D Matrix with Channel,Z,Y,X axes 
        :rtype: ndarray
        '''
        raise NotImplemented("Abstract base class")


def GetVolume(name):
    return models.Volume.objects.get(name=name)


class VolumeController(VolumeInterface):

    @property
    def name(self):
        return self.db_vol.name

    def __init__(self, db_vol):
        self.db_vol = db_vol

    @classmethod
    def Create(cls, name):
        db_vol = GetVolume(name)
        if db_vol is None:
            raise ValueError(name + " does not exist in database")

        obj = VolumeController(db_vol)
        
    def SetVolumeCoordSpace(self, coord_space):
        




def GetCoordSpace(volume_name, section_number, channel_name, transform_name):
    db_vol = GetVolume(volume_name)
    db_coordspace = models.CoordSpace.objects.get(name=models.CoordSpace.SectionChannelName(section_number, channel_name, transform_name))
    return db_coordspace

