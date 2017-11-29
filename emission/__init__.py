"""Emission python module

This module is for everyone who wants to build tools / systems for calculating vehicle
emissions for various types of vehicles (Trucks, Buses, Cars, Vans, scooters, ..).

The calculation and factors is provided by the EU EEA guidebook: http://www.eea.europa.eu/publications/emep-eea-guidebook-2016

Main features:
1. Give you the current emission for one or multiple types of pollutants for a given vehicle (check "emission.")
2. Given two points (UTM 33N coordinates - Norway) and a vehicle type, the module will use a 
   routing-service to calculate the best route to reach your destination. The module will also calculate the
   emission for all the pollutant types you have defined. You can then sort the various routes depending of
   which critieria that's most important (duration, pollution (NOx, CO, ..)).

Fuel consumption is directly related to the emission - therefore the lower emission the lower fuel consumption.
For the transportation industry this will be of great importance.
"""

import logging
log = logging.getLogger("emission")

from .Extrapolate import Extrapolate
from .Interpolate import Interpolate
from .Pollutants import Pollutants
from .EmissionJSONReader import EmissionsJsonParser
from .planner import Planner
from .planner import PollutantTypes

from .__version__ import  __version__

__author__ = "NPRA - Norwegian Public Roads Administration"

from .models import session
from . import models
from . import update_db as update