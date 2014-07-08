from django.contrib import admin
import nornir_djangomodel.models as models

admin.site.register(models.Dataset)
admin.site.register(models.Channel)
admin.site.register(models.Filter)
admin.site.register(models.CoordSpace)
admin.site.register(models.Mapping2D)
admin.site.register(models.Data2D)
admin.site.register(models.BoundingBox)