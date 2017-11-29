#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


# Meta-data
NAME = "emission"
DESCRIPTION = "Emission calculator library"
DESCRIPTION_OLD = """Emission calculator library to calculate total emissions
given a start and stop position. Various possible routes will be presented
sorted after the least pollutant route.

Vehicle types will be: personal cars, busses and trailers of different sizes.

NOTE that this extension only works for Norway, since we are using the
NPRA (Norwegian Public Roads Administration) road database https://www.vegvesen.no/nvdb/apidokumentasjon/
"""
URL = "https://github.com/NPRA/EmissionCalculatorLib"
EMAIL = "asbjorn@fellinghaug.com"
AUTHOR = """Juraj Cirbus <Juraj.Cirbus@norconsult.com>, Tomas Levin <tomas.levin@vegvesen.no>, Asbjørn Alexander Fellinghaug <asbjorn.fellinghaug@webstep.no>"""

REQUIRED = [
    'numpy',
    'SQLAlchemy',
    'six'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding="utf-8") as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


class PublishCommand(Command):
    """Support setup.py publish
    """

    description = 'Build and publish the package'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold"""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (univeral) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
        #os.system('twine upload dist/*')
        #sys.exit()

print("Version: {}".format(about['__version__']))


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    keywords="Emission calculation library using the NVDB (Norway)",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['emission'],
    install_requires=REQUIRED,
    package_data={
        'emission': ['*.json.gz', 'database.db'],
    },
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Office/Business'
    ],
    # $ setup.py publish support
    cmdclass={
        'publish': PublishCommand,
    },
)
