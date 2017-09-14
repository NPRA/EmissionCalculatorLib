import math
import json
try:
    from urllib.request import urlopen  # Python 3
except ImportError:
    from urllib import urlopen  # Python 2
import matplotlib.pyplot as plt
from optparse import OptionParser
import socket

from . import Pollutants
from . import EmissionsJsonReader


class EmissionCalculatorLib:
    def __init__(self):
        # init public values
        self.cumulative = False
        self.coordinates = ""
        self.calculate_nox = True
        self.calculate_co = True
        self.calculate_hc = True
        self.calculate_pm = True
        self.calculate_fc = True
        self.paths = []
        self.emissionJson = EmissionsJsonReader()
        self.show_in_graph = True
        self.length = "12"
        self.height = "4.4"

        self.roads_distances = []
        self.emission_summary = {}

        # temp values
        self._json_data = {}

    def _init_emission_dict(self):
        self.pollutants = Pollutants(len(self.paths))
        self.pollutants.add_pollutant("FC", self.calculate_fc)
        self.pollutants.add_pollutant("PM", self.calculate_pm)
        self.pollutants.add_pollutant("HC", self.calculate_hc)
        self.pollutants.add_pollutant("CO", self.calculate_co)
        self.pollutants.add_pollutant("NOx", self.calculate_nox)
        if (len(self.pollutants)) == 0:
            self.show_in_graph = False

    def _reinit_temp_values(self):
        self.atr_distances = []
        self.atr_times = []
        # re-init paths
        self.paths = []

    def get_json_from_url(self):
        load = self.emissionJson.load
        socket.setdefaulttimeout(30)
        try:
            url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=270337.81,7041814.57%3B296378.67,7044118.5&weight=50&geometryformat=isoz"
            # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height="+self.height+"&lang=nb-no&length="+self.length+"&stops="+self.coordinates+"&weight="+load+"&geometryformat=isoz"
            # url with 3 roads from Oslo to Molde
            # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=262210.96,6649335.15%3B96311.150622257,6969883.5407672&weight=50&geometryformat=isoz"
            response = urlopen(url)
            self._json_data = json.loads(response.read())
            self.set_data(self._json_data)
        except:
            self.emission_summary["Fail"] = "Fail to load data from url."


    def get_json_data(self):
        return self._json_data

    def set_data(self, json_data):
        self._reinit_temp_values()
        if "messages" not in json_data:
            for i in range(len(json_data["routes"]["features"])):
                self.atr_distances.append(json_data["routes"]["features"][i]['attributes']["Total_Meters"])
                self.atr_times.append(json_data["routes"]["features"][i]['attributes']["Total_Minutes"])
                self.paths.append(json_data["routes"]["features"][i]["geometry"]["paths"][0])
        else:
            print (json_data["messages"][0]['description'])
            self.emission_summary["Fail"] = json_data["messages"][0]['description']

    @staticmethod
    def _get_distance_2d(point1, point2):
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return distance

    @staticmethod
    def _get_distance_3d(point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)
        return distance

    def _get_slope(self, point1, point2):
        distance = self._get_distance_3d(point1, point2)
        slope = 0.0
        if distance != 0:
            slope = math.degrees(math.asin((float(point2[2])- float(point1[2]))/distance))
        return slope

    def _get_velocity(self, index):
        dist = self.atr_distances[index]
        time = 60 * self.atr_times[index]
        return (dist/time) * 3.6

    def calculate_emissions(self):
        self.roads_distances = []
        self._init_emission_dict()

        for j in range(len(self.paths)):
            distances = []
            self.emissionJson.velocity = self._get_velocity(j)
            for i in range(len(self.paths[j])):
                if (i + 1) < len(self.paths[j]):
                    if len(distances) > 0:
                        distances.append(distances[-1] + self._get_distance_3d(self.paths[j][i], self.paths[j][i + 1]) / 1000)
                    else:
                        distances.append(self._get_distance_3d(self.paths[j][i], self.paths[j][i + 1]) / 1000)
                    self.emissionJson.slope = self._get_slope(self.paths[j][i], self.paths[j][i + 1])
                    for pollutant in self.pollutants:
                        calc_emission = self.emissionJson.get_emission_for_pollutant(pollutant)
                        if len(self.pollutants[pollutant][j]) > 0 and self.cumulative:
                            result_emission = self.pollutants[pollutant][j][
                                                  -1] + calc_emission
                        else:
                            result_emission = calc_emission
                        self.pollutants[pollutant][j].append(result_emission)
            self.roads_distances.append(distances)

    def show_emissions(self):
        self.emission_summary = {}
        if self.show_in_graph:
            fig = plt.figure()
            figs = []
            pollutant_counter = 0
            for pollutant in self.pollutants:
                pollutant_counter += 1
                num_plots = 100 * len(self.pollutants._pollutants) + 10 + pollutant_counter
                ax = fig.add_subplot(num_plots)
                ax.set_title(pollutant)
                ax.set_ylim(0, max(max(self.pollutants[pollutant])) + 1)
                figs.append(ax)

            for i in range(len(self.paths)):
                pollutant_counter = 0
                self.emission_summary[i + 1] = {}
                for pollutant in self.pollutants:
                    ax = figs[pollutant_counter]
                    ax.plot(self.roads_distances[i], self.pollutants[pollutant][i])
                    pollutant_counter += 1
                    if self.cumulative:
                        self.emission_summary[i + 1][pollutant] = max(self.pollutants[pollutant][i])
                    else:
                        self.emission_summary[i + 1][pollutant] = sum(self.pollutants[pollutant][i])

            # print (self.emission_summary)
            ax = figs[-1]
            labels = ["Route " + str(i+1) for i in range(len(self.paths))]
            pos = (len(figs)/10.0) * (-1)
            ax.legend(labels, loc=(0, pos), ncol = len(self.paths))
            plt.show()
        else:
            for i in range(len(self.paths)):
                self.emission_summary[i + 1] = {}
                for pollutant in self.pollutants:
                    if self.cumulative:
                        self.emission_summary[i + 1][pollutant] = max(self.pollutants[pollutant][i])
                    else:
                        self.emission_summary[i + 1][pollutant] = sum(self.pollutants[pollutant][i])
            # print (self.emission_summary)

    def get_summary(self):
        return self.emission_summary

if __name__ == "__main__":
    VERSION = "0.1.0"
    description = "Emission Calculator Lib"
    parser = OptionParser(usage="usage: % prog [options] start<startCoord> end<endCoord> length<length> height<height> "
                                "load<load> input<inputFile> nox<nox> co<co> hc<hc> pm<pm> fc<fc> "
                                "cumulative<cumulative> graph<graph>",
                          version="%prog " + VERSION + ", Copyright (c) TRAN",
                          description=description, add_help_option=True)

    parser.add_option("--start", dest="startCoord", default=[0,0], help='Set start coordinates', metavar="Array")
    parser.add_option("--end", dest="endCoord", default=[0,0], help='Set end coordinates', metavar="Array")
    parser.add_option("--length", dest="length", default=12, help='Vehicle length', metavar="Value")
    parser.add_option("--height", dest="height", default=4.4, help='Vehicle height', metavar="Value")
    parser.add_option("--load", dest="load", default=0, help="Vehicle load")
    parser.add_option("--input", dest="inputFile", default="inputData.txt", help='Set type vehicle motor, this is necessary for'
                                                                     ' calculate emission', metavar="String")
    parser.add_option("--nox", dest="nox", default=False, help='Get NOx emissions', metavar="Bool")
    parser.add_option("--co", dest="co", default=True, help='Get CO emissions', metavar="Bool")
    parser.add_option("--hc", dest="hc", default=False, help='Get HC emissions', metavar="Bool")
    parser.add_option("--pm", dest="pm", default=False, help='Get PM emissions', metavar="Bool")
    parser.add_option("--fc", dest="fc", default=False, help='Get FC emissions', metavar="Bool")
    parser.add_option("--cumulative", dest="cumulative", default=False, help='Cumulative curve in graph', metavar="Bool")
    parser.add_option("--graph", dest="graph", default=True, help='Show results in graph', metavar="Bool")

    (options, args) = parser.parse_args()

    emission_calculator = EmissionCalculatorLib()

    coordinates = str(options.startCoord[0])+","+str(options.startCoord[1])+";"+str(options.endCoord[0])+","+str(options.endCoord[1])
    emission_calculator.coordinates = coordinates
    emission_calculator.length = str(options.length)
    emission_calculator.height = str(options.height)
    emission_calculator.load = str(options.load)

    emission_calculator.get_json_from_url()

    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    if len(emission_calculator.paths) > 0:
        emission_calculator.calculate_nox = str2bool(str(options.nox))
        emission_calculator.calculate_co = str2bool(str(options.co))
        emission_calculator.calculate_hc = str2bool(str(options.hc))
        emission_calculator.calculate_pm = str2bool(str(options.pm))
        emission_calculator.calculate_fc = str2bool(str(options.fc))

        emission_calculator.cumulative = str2bool(str(options.cumulative))
        emission_calculator.show_in_graph = str2bool(str(options.graph))

        for i in range(len(emission_calculator.atr_distances)):
            distance = emission_calculator.atr_distances[i] / 1000
            hours, minutes = divmod(emission_calculator.atr_times[i], 60)
            hours = int(hours)
            minutes = int(minutes)
            print ("Route " + str(i + 1))
            print ("Length: " + str(distance) + " km, driving time: " + str(hours) + " hours and " + str(
                    minutes) + " minutes.")
        if options.inputFile != "":
            emission_calculator.emissionJson.read_data_from_input_file(options.inputFile)
            emission_calculator.calculate_emissions()
            emission_calculator.show_emissions()
            print emission_calculator.get_summary()