"""Emission python module"""

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