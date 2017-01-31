'''
Created on Aug 30, 2013

@author: u0490822
'''




# from ez_setup import use_setuptools
# from setuptools import setup, find_packages
import glob
import os

from ez_setup import use_setuptools


if __name__ == '__main__':
    use_setuptools()

    from setuptools import setup, find_packages

    packages = find_packages()

    install_requires = ["django>=1.6.5",
                        "nornir_djangomodel>=1.2.0"]

    dependency_links = ["git+http://github.com/nornir/nornir-djangomodel#egg=nornir_djangomodel-1.2.0"]

    scripts = None

    classifiers = ['Programming Language :: Python :: 3.4',
                   'Topic :: Scientific/Engineering']

    setup(name='nornir_web',
          classifiers=classifiers,
          version='1.3.0',
          description="Django web modules for Nornir",
          author="James Anderson",
          author_email="James.R.Anderson@utah.edu",
          url="https://github.com/nornir/nornir-web",
          packages=packages,
          scripts=scripts,
          test_suite='test',
          install_requires=install_requires,
          dependency_links=dependency_links)
