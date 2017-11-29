import json
try:
    from urllib.request import urlopen  # Python 3
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen  # Python 2
    from urllib import urlencode
import socket
import math

from . import vehicles, log
from . import EmissionsJsonParser
from .exceptions import RouteError
from . import models


def enum(**named_values):
    return type('Enum', (), named_values)


# List of possible pollutant types
PollutantTypes = enum(
    CH4='CH4',
    CO='CO',
    EC='EC',
    NOx='NOx',
    PM_EXHAUST='PM Exhaust',
    VOC='VOC')

# URL to remote route webservice
ROUTE_URL_BASE = "https://www.vegvesen.no/ws/no/vegvesen/ruteplan/routingService_v1_0/routingService/"


class Route:
    """Represent a route object from the NVDB RoutingService"""

    def __init__(self, distance, minutes, path, id):
        self.distance = distance
        self.minutes = minutes
        self.path = path
        self.pollutants = {}
        self.distances = []
        self.id = id

    def hours_and_minutes(self):
        """Return hours:minutes as a string
        representation, based on the total amount
        of minutes for the route.
        """
        hours, minutes = divmod(self.minutes, 60)
        return "{}:{}".format(hours, minutes)

    def velocity(self):
        """Calculate the velocity
        """
        total_time = self.minutes * 60
        return (self.distance / total_time) * 3.6

    def add_pollutant(self, p, calc_emission):
        if p not in self.pollutants:
            self.pollutants[p] = []

        self.pollutants[p].append(calc_emission)

    def add_distances(self, distances):
        self.distances.append(distances)

    def total_emission(self, pollutant):
        total = sum(self.pollutants[pollutant])
        return total

    def __repl__(self):
        fmt = "Route(distance={}, minutes={})"
        return fmt.format(self.distance, self.minutes)

    def __str__(self):
        return self.__repl__()

    def __eq__(self, other):
        return self.minutes == other.minutes

    def __lt__(self, other):
        return self.minutes < other.minutes


class RouteSet:
    """A collection of Route objects"""

    def __init__(self, routes=None):
        if routes is None:
            self._lst = []
        else:
            self._lst = routes

    def __getitem__(self, item):
        return self._lst[item]

    def __iter__(self):
        return iter(self._lst)

    def __len__(self):
        return len(self._lst)

    def add(self, route):
        self._lst.append(route)

    def __repl__(self):
        return "RouteSet({})".format("\n".join([str(r) for r in self._lst]))

    def __str__(self):
        return self.__repl__()

    def sort(self, key=None, reverse=False):
        self._lst.sort(key=key, reverse=reverse)

    def __hash__(self):
        return hash(self._lst)


class Planner:
    """This class takes a start, stop and vehicle input to give the user
    a set of possible road routes sorted after the least pollution. Also
    more metadata about each route is provided.
    """

    def __init__(self, start, stop, vehicle):
        self._start = start
        self._stop = stop

        if not isinstance(vehicle, vehicles.Vehicle):
            raise ValueError("Vehicle is not of correct type. Check vehicle implementations.")
        self._vehicle = vehicle
        # self._emissionJson = EmissionsJsonParser(vehicle)
        # self._emissionJson._init_values_from_input_file()
        self._emissionDb = None  # EmissionsJsonParser(self._vehicle)
        self.routes = RouteSet()

        self._pollutants = {}

    @property
    def pollutants(self):
        return self._pollutants

    def add_pollutant(self, pollutant_type):
        # validate input
        if pollutant_type not in PollutantTypes.__dict__.values():
            raise ValueError("pollutant_type needs to be one of the types defined in planner.PollutantTypes")

        if pollutant_type not in self._pollutants:
            self._pollutants[pollutant_type] = None
        else:
            log.debug("warning: pollutant already added..")
        log.debug("self._pollutants = {}".format(self._pollutants))

    @property
    def coordinates(self):
        return "{start[0]},{start[1]};{end[0]},{end[1]}".format(
            start=self._start, end=self._stop)

    @staticmethod
    def build_url(vehicle, coordinates, format="json", geometryformat="isoz"):
        """Construct a well formed url for the routing service which
        NPRA is using.
        """
        load = vehicle.load if vehicle.load > -1.0 else 0
        params = {
            "format": format,
            "height": vehicle.height,
            "length": vehicle.length,
            "stops": coordinates,
            "load": load,
            "geometryformat": geometryformat,
            "lang": "nb-no",
        }

        return '?'.join([ROUTE_URL_BASE, urlencode(params)])

    def _get_routes(self):
        socket.setdefaulttimeout(30)
        try:
            url = Planner.build_url(self._vehicle, self.coordinates)
            log.debug("Calling: {}".format(url))
            log.debug("coordinates: {}".format(self.coordinates))
            response = urlopen(url)
            data = response.read()
            self._json_data = json.loads(data.decode("utf-8"))
            if 'messages' in self._json_data:
                raise RouteError("Missing 'messages' in returned JSON data.")

        except IOError as err:
            log.debug("ioerror: {}".format(err))
            self._json_data = {}
            raise RouteError("IOError: {}".format(err))

        except ValueError:
            log.warning("Bad data from remote routing service: \n{}".format(data))
            self._json_data = {}
            raise RouteError("Bad data from remote routing service: \n{}".format(data))

    @staticmethod
    def _get_distance_2d(point1, point2):
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return distance

    @staticmethod
    def _get_distance_3d(point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)
        return distance

    @staticmethod
    def _get_slope(point1, point2):
        distance = Planner._get_distance_3d(point1, point2)
        slope = 0.0
        if distance:
            slope = math.degrees(math.asin((float(point2[2]) - float(point1[2])) / distance))
        return slope

    def _get_pollutants_for_vehicle(self):
        """Retrieve pollutions parameters for the vehicle provided
        to the planner. Only include the pollutants provided in
        'self._pollutants'
        """
        from . import session

        category = models.Category.get_for_type(self._vehicle)
        if not category:
            raise ValueError("Unable to find Category for vehicle: {}".format(category))

        fuel = session.query(models.Fuel).filter_by(name=self._vehicle.fuel_type).first()
        if not fuel:
            raise ValueError("Unable to find Fuel in database: name={}".format(self._vehicle.fuel_type))

        segment = session.query(models.Segment).filter_by(name=self._vehicle.segment).first()
        if not segment:
            raise ValueError("Unable to find segment in database: name={}".format(str(self._vehicle.segment)))

        filter_parms = {
            "category": category,
            "fuel": fuel,
            "segment": segment
        }

        euro_std = session.query(models.EuroStd).filter_by(name=self._vehicle.euro_std).first()
        if euro_std:
            filter_parms.update({"eurostd": euro_std})

        mode = session.query(models.Mode).filter_by(name=self._vehicle.mode).first()
        if mode:
            filter_parms.update({"mode": mode})

        if self._vehicle.load > -1.0:
            filter_parms.update({"load": self._vehicle.load})

        # Get Parameters based on the other items found above
        params = session.query(models.Parameter).filter_by(**filter_parms)
        return params.all()

    def get_emission(self, parameters, slope=None):
        pollutant = None

        if len(parameters) > 1:
            # We have many parameters instances for a single pollutant.
            # This means that we have multiple 'slopes' in our table.
            # Need therefore to find slope or extrapolate/interpolate the value.
            positive_slopes = [0, 0.02, 0.04, 0.06]
            negative_slopes = [-0.06, -0.04, -0.02, 0]

            x = [x for x in parameters if x.slope == slope]
            if any(x):
                pollutant = x[0]
            else:
                slopes_for_pollutant = []
                if slope > 0.0:
                    tmp_pollutants = [x for x in parameters if x.slope in positive_slopes]
                    slopes_for_pollutant = map(Planner.calculate, tmp_pollutants)
                    extrapolate = Extrapolate(positive_slopes, slopes_for_pollutant)
                    tmp = extrapolate[slope]
                    log.debug("Extrapolated value: {}".format(tmp))
                    return tmp

                else:
                    tmp_pollutants = [x for x in parameters if x.slope in negative_slopes]
                    slopes_for_pollutant = map(Planner.calculate, tmp_pollutants)
                    interpolate = Interpolate(negative_slopes, slopes_for_pollutant)
                    tmp = interpolate[slope]
                    log.debug("Interpolated value: {}".format(tmp))
                    return tmp
        else:
            pollutant = parameters[0]
        tmp = Planner.calculate(pollutant)
        log.debug("tmp: {}".format(tmp))
        return tmp

    @staticmethod
    def calculate(parameter):
        """Equation copied from the EU spreadsheet
        """
        alpha = parameter.ALPHA
        beta = parameter.BETA
        delta = parameter.DELTA
        epsilon = parameter.EPSILON
        gamma = parameter.GAMMA
        hta = parameter.HTA
        reduct_fact = parameter.REDUCTIONFACTOR
        speed = parameter.SPEED
        v_max = parameter.MAXSPEED
        v_min = parameter.MINSPEED
        zita = parameter.ZITA

        """ ((alpha*speed^2) + (beta*speed) + gamma + (delta/speed))/((epsilon*speed^2) * (zita * speed + htz))"""
        result = (alpha * math.pow(speed, 2)) + (beta * speed) + gamma + (delta / speed)
        result /= (epsilon * math.pow(speed, 2)) + ((zita * speed) + hta)
        result *= (1 - reduct_fact)
        return result

    def _calculate_emissions(self):
        """Calculate total emission from a route of x,y,z points based on a path between 
        two points (A -> B). https://www.vegvesen.no/vegkart/vegkart/.

        For a simple static emission calculation play with:
            - self._get_pollutants_for_vehicle()
            - Planner.calculate(parameter)
        """
        parameters = self._get_pollutants_for_vehicle()

        self.routes = RouteSet()

        if "routes" not in self._json_data:
            log.debug("Error in returned JSON data from web service.")
            log.debug("data: {}".format(self._json_data))
            return

        # Create a "set" of Routes. The planner web service will
        # return 2-4 routes with different paths.
        for idx, r in enumerate(self._json_data["routes"]["features"]):
            attributes = r.get("attributes")
            route = Route(distance=attributes.get("Total_Meters"),
                          minutes=attributes.get("Total_Minutes"),
                          path=r.get("geometry").get("paths")[0], id = idx)
            self.routes.add(route)

        log.debug("Nr of routes: {}".format(len(self.routes)))
        for i, route in enumerate(self.routes):
            # A list of x,y,z points that all together represents the route
            path_coordinates = route.path
            distances = []

            # Nifty little trick to loop over 'path_coordinates',
            # but keep a reference to the 'prev' item to calculate the
            # distance between them
            iter_points = iter(path_coordinates)
            prev = next(iter_points)
            for point in path_coordinates:
                if not distances:
                    # first point
                    distances.append(Planner._get_distance_3d(prev, point) / 1000)
                else:
                    distances.append(distances[-1] + Planner._get_distance_3d(prev, point) / 1000)

                point_slope = Planner._get_slope(prev, point)

                # Calculate emission for each pollutants the user has asked for
                for p in self._pollutants:
                    parms = [x for x in parameters if x.pollutant.name.startswith(p)]
                    calc_emission = self.get_emission(parms, point_slope)
                    route.add_pollutant(p, calc_emission)

                prev = point

            route.add_distances(distances)

    def run(self):
        """
        Use the input data and send a HTTP request to route planner.
        Construct a 'Routes' object containing all the possible 'Route' objects.

        Also compute the pollution factor for each route based on the 'Route' data and
        the vehicle choosen.
        """

        self._get_routes()
        self._calculate_emissions()
