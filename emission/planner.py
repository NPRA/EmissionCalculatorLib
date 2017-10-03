import json
try:
    from urllib.request import urlopen  # Python 3
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen  # Python 2
    from urllib import urlencode
import socket
import math
import six

from . import vehicles
from . import EmissionsJsonReader, EmissionsJsonParser
from .exceptions import RouteError
from . import Pollutants


def enum(**named_values):
    return type('Enum', (), named_values)


# List of possible pollutions
PollutantTypes = enum(
    CH4='CH4',
    CO='CO',
    EC='EC',
    NOx='NOx',
    PM_EXHAUST='PM Exhaust',
    VOC='VOC')

# URL to remote route webservice
ROUTE_URL_BASE = "http://multirit.triona.se/routingService_v1_0/routingService/"


class Route:
    """Represent a route object from NVDB RoutingService
    """
    def __init__(self, distance, minutes, path):
        self.distance = distance
        self.minutes = minutes
        self.path = path
        self.pollutants = {}
        self.distances = []

    def hours_and_minutes(self):
        """Return hours:minutes as a string
        representation, based on the total amount
        of minutes for the route.
        """
        hours, minutes = divmod(self.minutes, 60)
        return "{}:{}".format(hours, minutes)

    def velocity(self):
        """n/a
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
        # emissions = ""
        # for p in self.pollutants:
        #     emissions += "{}={} ".format(p, self.pollutants[p])
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

    def sort(self, cmp=None, key=None, reverse=False):
        self._lst.sort(cmp, key, reverse)

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
        if pollutant_type not in PollutantTypes.__dict__:
            raise ValueError("pollutant_type needs to be one of the types defined in planner.PollutantTypes")

        if pollutant_type not in self._pollutants:
            self._pollutants[pollutant_type] = None
        else:
            print("warning: pollutant already added..")
        print("self._pollutants = {}".format(self._pollutants))

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
            # "height": vehicle.height,
            # "length": vehicle.length,
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
            print("Calling: {}".format(url))
            print("coordinates: {}".format(self.coordinates))
            response = urlopen(url)
            self._json_data = json.loads(response.read())
            if 'messages' in self._json_data:
                raise RouteError("")
        except IOError as err:
            print("ioerror: {}".format(err))
            self._json_data = {}

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

    def _calculate_emissions(self):
        self.routes = Routes()

        for r in self._json_data["routes"]["features"]:
            attributes = r.get("attributes")
            route = Route(distance=attributes.get("Total_Meters"),
                          minutes=attributes.get("Total_Minutes"),
                          path=r.get("geometry").get("paths")[0])
            self.routes.add(route)

        print("Nr of routes: {}".format(len(self.routes)))

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

                # TODO: Refactore this, so that we pass the 'slope' value
                #       in when getting the emission for the pollutant
                print("prev: " + str(prev))
                print("point: " + str(point))
                self._emissionDb.slope = Planner._get_slope(prev, point)

                # Calculate pollutants
                """
                for pollutant in self.pollutants:
                        calc_emission = self.emissionJson.get_emission_for_pollutant(pollutant)
                        if len(self.pollutants[pollutant][j]) > 0 and self.cumulative:
                            result_emission = self.pollutants[pollutant][j][-1] + calc_emission
                        else:
                            result_emission = calc_emission
                        self.pollutants[pollutant][j].append(result_emission)
                """

                for p in self._pollutants:
                    # if not self._pollutants[p]:
                    #    self._pollutants[p] = [[] for _ in range(len(self.routes))]

                    # calc_emission = self._emissionJson.get_emission_for_pollutant(p)
                    calc_emission = self._emissionDb.get_for_pollutant(p)
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
        print("Done! Loop over '.routes'")

        print("Routes: {}".format(self.routes))
