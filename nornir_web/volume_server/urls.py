from django.conf.urls import patterns, include, url
from . import viking_views, views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.DatasetIndexView.as_view(), name='index'),
                       url(r'^(?P<dataset_name>.+)/(?P<coordspace_name>.+)/bounds', views.get_bounds, name='get_bounds'),
                       url(r'^(?P<dataset_name>.+)/(?P<section_number>\d+)/(?P<channel_name>.+)/(?P<downsample>\d+)/(.*_)?X(?P<column>\d+)_Y(?P<row>\d+).png$', viking_views.get_tile, name='get_tile'),
                       # url(r'^(?P<dataset_name>.+)/(?P<channel_name>.+)/$', views.get_image, name='get_image'),
                       # url(r'^(?P<dataset_name>.+)/$', views.image_form, name='image_form')

    # Examples:
    # url(r'^$', 'nornir_web.views.home', name='home'),
    # url(r'^nornir_web/', include('nornir_web.nornir_web.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
