from django.conf import settings

'''
List of directories that may contain volumes
'''
VOLUME_IMPORTER_VOLUME_DIRS = getattr(settings, "VOLUME_IMPORTER_VOLUMEDIR", [])