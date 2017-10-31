"""Emission python module 
"""

import logging

from .Extrapolate import Extrapolate
from .Interpolate import Interpolate
from .Pollutants import Pollutants
from .EmissionJSONReader import EmissionsJsonParser
from .planner import Planner
from .planner import PollutantTypes

from .__version__ import  __version__

__author__ = "NPRA - Norwegian Public Roads Administration"

log = logging.getLogger("emission")