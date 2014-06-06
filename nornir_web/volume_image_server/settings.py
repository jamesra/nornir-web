from django.conf import settings

'''
List of directories that may contain volumes
'''
VOLUME_IMAGE_SERVER_VOLUME_DIRS = getattr(settings, "VOLUME_IMAGE_SERVER_VOLUMEDIR", [])

VOLUME_IMAGE_SERVER_IMAGE_ROOT =  getattr(settings, "VOLUME_IMAGE_SERVER_IMAGE_ROOT", 'C:\\inetpub\\wwwroot\\volume_image_server\\images')
VOLUME_IMAGE_SERVER_IMAGE_URL = getattr(settings, "VOLUME_IMAGE_SERVER_IMAGE_URL", 'http://localhost/volume_image_server/images')

VOLUME_IMAGE_SERVER_TILE_WIDTH =  getattr(settings, "TILE_WIDTH", 256)
VOLUME_IMAGE_SERVER_TILE_HEIGHT = getattr(settings, "TILE_HEIGHT", 256)

VOLUME_IMAGE_SERVER_TILE_CACHE_ROOT = getattr(settings, "VOLUME_TILE_CACHE_ROOT", 'C:\\inetpub\\wwwroot\\volume_image_server\\tiles')
VOLUME_IMAGE_SERVER_TILE_CACHE_URL = getattr(settings, "VOLUME_TILE_CACHE_SERVER_IMAGE_URL", 'http://localhost/volume_image_server/tiles')

VOLUME_IMAGE_SERVER_TILE_CACHE_ENABLED = True