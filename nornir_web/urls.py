from django.conf.urls import patterns, include, url
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^volume_image_server/', include('nornir_web.volume_image_server.urls', namespace="volume_image_server", app_name="volume_image_server")),
                       # url(r'^volumes/', include('nornir_web.volume_importer.urls', namespace="volume_importer", app_name="volume_importer")),
                       url(r'^volume_server/', include('nornir_web.volume_server.urls', namespace="volume_server", app_name="volume_server")),
    # Examples:
    # url(r'^$', 'nornir_web.views.home', name='home'),
    # url(r'^nornir_web/', include('nornir_web.nornir_web.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
