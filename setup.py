#! /usr/bin/env python
#
# Copyright (C) 2018 Python Charmers Pty Ltd, Australia

import os

DESCRIPTION = "starborn: statistical data visualization with Vega"
LONG_DESCRIPTION = """\
Starborn is a library for making attractive and informative statistical
graphics in Python. It aims to be API-compatible with Seaborn but built on top
of Altair.
"""
DISTNAME = 'starborn'
MAINTAINER = 'Ed Schofield'
MAINTAINER_EMAIL = 'ed@pythoncharmers.com'
URL = 'https://github.io/edschofield/starborn'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/edschofield/starborn/'
VERSION = '0.1'

INSTALL_REQUIRES = [
    'altair>=2.0',
]

PACKAGES = [
    'starborn',
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: BSD License',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Multimedia :: Graphics',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
    'Operating System :: Windows'
]

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
    )
