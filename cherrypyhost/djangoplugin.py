# -*- coding: utf-8 -*-
import imp
import os, os.path
import sys

import cherrypy
from cherrypy.process import plugins
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

import httplogger


__all__ = ['DjangoAppPlugin']

class DjangoAppPlugin(plugins.SimplePlugin):
    def __init__(self, bus, wsgi_http_logger=httplogger.HTTPLogger):
        """ CherryPy engine plugin to configure and mount
        the Django application onto the CherryPy server.
        """
        plugins.SimplePlugin.__init__(self, bus) 
        self.wsgi_http_logger = wsgi_http_logger

    def start(self):
        """ When the bus starts, the plugin is also started
        and we load the Django application. We then mount it on
        the CherryPy engine for serving as a WSGI application.
        We let CherryPy serve the application's static files.
        """
        cherrypy.log("Loading and serving the Django application")
        cherrypy.tree.graft(self.wsgi_http_logger(WSGIHandler()))
        settings = self.load_settings() 
#
        static_handler = cherrypy.tools.staticdir.handler(
            section="/",
            dir=os.path.split(settings.STATIC_ROOT)[1],
            root=os.path.abspath(os.path.split(settings.STATIC_ROOT)[0])
        )
        cherrypy.tree.mount(static_handler, settings.STATIC_URL)
        
    @classmethod
    def get_settings_from_module(cls, name):
        
        fd, path, description = (None, None, None)
        if '.' in name:
            package, mod = name.rsplit('.', 1)
            fd, path, description = imp.find_module(mod)
        else:
            mod = name
            package = None
            fd, path, description = imp.find_module(mod)
        
        try:
            return imp.load_module(mod, fd, path, description)
        finally:
            if fd: fd.close()
                    

    def load_settings(self):
        """ Loads the Django application's settings. You can
        override this method to provide your own loading
        mechanism. Simply return an instance of your settings module.
        """
 
        name = None
        path = None
        if len(sys.argv) > 1:
            name = sys.argv[1]
            os.environ['DJANGO_SETTINGS_MODULE'] = name
            if len(sys.argv) > 2:
                path = sys.argv[2]
                if os.path.isdir(path):
                    sys.path.append(path)
                else:
                    print("Settings module path is not a valid directory: %s" % (path))
                    sys.exit()
        elif 'DJANGO_SETTINGS_MODULE' in os.environ:
            name = os.environ['DJANGO_SETTINGS_MODULE']
        else:
            print("Settings module must be first argument or specified in DJANGO_SETTINGS_MODULE environment variable")
            sys.exit()
            
            
        return self.get_settings_from_module(name)
        
