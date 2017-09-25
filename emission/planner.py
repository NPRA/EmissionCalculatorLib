import json
try:
    from urllib.request import urlopen  # Python 3
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen  # Python 2
    from urllib import urlencode
import socket
import math

from . import vehicles
from . import EmissionsJsonReader
from .exceptions import RouteError

ROUTE_URL_BASE = "http://multirit.triona.se/routingService_v1_0/routingService/"


class Route:
    """Represent a route object from NVDB RoutingService
    """
    def __init__(self, distance, minutes, path):
        self.distance = distance
        self.minutes = minutes
        self.path = path
        self.emission = None

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


class Routes:
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

        self._emissionJson = EmissionsJsonReader()

        self.routes = Routes()

        # Get remote JSON webservice data with routes
        # self._get_routes()
        self._init_pollutants()

    def _init_pollutants(self):
        self._pollutants = Pollutants()

    @property
    def coordinates(self):
        return "{start[0]},{start[1]};{end[0]},{end[1]}".format(
            start=self._start, end=self._stop)

    @staticmethod
    def build_url(vehicle, coordinates, format="json", geometryformat="isoz"):
        """Construct a well formed url for the routing service which
        NPRA is using.
        """
        params = {
            "format": format,
            "height": vehicle.height,
            "length": vehicle.length,
            "stops": coordinates,
            "load": vehicle.load,
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
            slope = math.degrees(math.asin(float(point2[2]) - float(point1[2])) / distance)
        return slope

    def _calculate_emissions(self):
        self.routes = Routes()

        for r in self._json_data["routes"]["features"]:
            attributes = r.get("attributes")
            route = Route(distance=attributes.get("Total_Meters"),
                          minutes=attributes.get("Total_Minutes"),
                          path=r.get("geometry").get("paths")[0])
            self.routes.add(route)

        print("Nr of routes: " + len(self.routes))

        for r in self.routes:
            # A list of x,y,z points that all together represents the route
            path_coordinates = r.path
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
                    distances.append(distances[-1], Planner._get_distance_3d(prev, point) / 1000)

                self._emissionJson.slope = Planner._get_slope(prev, point)

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

                prev = point

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