from django.conf import settings

'''
List of directories that may contain volumes
'''
VOLUME_SERVER_COORD_SPACE_NAME = getattr(settings, "VOLUME_SERVER_COORD_SPACE_NAME", "ChannelToVolume")
VOLUME_SERVER_COORD_SPACE_RESOLUTION = getattr(settings, "VOLUME_SERVER_COORD_SPACE_RESOLUTION", 2.176)

VOLUME_SERVER_TILE_WIDTH = getattr(settings, "TILE_WIDTH", 256)
VOLUME_SERVER_TILE_HEIGHT = getattr(settings, "TILE_HEIGHT", 256)

VOLUME_SERVER_TILE_CACHE_ROOT = getattr(settings, "VOLUME_SERVER_TILE_CACHE_ROOT", 'C:\\inetpub\\wwwroot\\volume_server\\tiles')
VOLUME_SERVER_TILE_CACHE_URL = getattr(settings, "VOLUME_SERVER_TILE_CACHE_SERVER_IMAGE_URL", 'http://localhost/volume_server/tiles')

VOLUME_SERVER_TILE_CACHE_ENABLED = True