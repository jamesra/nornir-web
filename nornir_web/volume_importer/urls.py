from django.conf.urls import patterns, include, url

from . import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('', 
                       url(r'^$', views.IndexView.as_view(), name='index'), 
    # Examples:
    # url(r'^$', 'nornir_web.views.home', name='home'),
    # url(r'^nornir_web/', include('nornir_web.nornir_web.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
