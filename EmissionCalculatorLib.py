import math
import json
try:
    from urllib.request import urlopen  # Python 3
except ImportError:
    from urllib import urlopen  # Python 2
from EmissionJSONReader import EmissionsJsonReader
import matplotlib.pyplot as plt
from optparse import OptionParser


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
        self.height = "4.5"
        # self.vehicle_load = "50"
        # self.vehicle_load = self.emissionJson.load

        # private values
        self.__pollutants = ["NOx", "CO", "HC", "PM", "FC"]

        # self.__emissions_for_pollutant = {}

        # temp values
        # self.__atributes = {}
        # self.atr_distances = []
        # self.atr_times = []
        # self.statistics = {}

    def __init_emission_dict(self):
        self.__emissions_for_pollutant = {}
        if self.calculate_nox:
            self.__emissions_for_pollutant["NOx"] = []
        if self.calculate_co:
            self.__emissions_for_pollutant["CO"] = []
        if self.calculate_hc:
            self.__emissions_for_pollutant["HC"] = []
        if self.calculate_pm:
            self.__emissions_for_pollutant["PM"] = []
        if self.calculate_fc:
            self.__emissions_for_pollutant["FC"] = []
        self.__init_emission_dict_with_paths(len(self.paths))

    def __init_emission_dict_with_paths(self, paths_count):
        for i in range(len(self.__emissions_for_pollutant)):
            pollutant_key = list(self.__emissions_for_pollutant.keys())[i]
            for j in range(paths_count):
                self.__emissions_for_pollutant[pollutant_key].append([])

    def __init_temp_values(self):
        self.atr_distances = []
        self.atr_times = []
        self.statistics = {}
        # re-init paths
        self.paths = []

    def get_json_from_url(self):
        self.__init_temp_values()
        load = self.emissionJson.load
        # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=270337.81,7041814.57%3B296378.67,7044118.5&weight=50&geometryformat=isoz"
        url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height="+self.height+"&lang=nb-no&length="+self.length+"&stops="+self.coordinates+"&weight="+load+"&geometryformat=isoz"
        # url with 3 roads from Oslo to Molde
        # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=262210.96,6649335.15%3B96311.150622257,6969883.5407672&weight=50&geometryformat=isoz"
        response = urlopen(url)
        data = json.loads(response.read())
        if "messages" not in data:
            for i in range(len(data["routes"]["features"])):
                self.atr_distances.append(data["routes"]["features"][i]['attributes']["Total_Meters"])
                self.atr_times.append(data["routes"]["features"][i]['attributes']["Total_Minutes"])
                self.paths.append(data["routes"]["features"][i]["geometry"]["paths"][0])
        else:
            print data["messages"][0]['description']

    @staticmethod
    def __get_distance_2d(point1, point2):
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return distance

    @staticmethod
    def __get_distance_3d(point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)
        return distance

    def __get_slope(self, point1, point2):
        distance = self.__get_distance_3d(point1, point2)
        slope = 0.0
        if distance != 0:
            slope = math.degrees(math.asin((float(point2[2])- float(point1[2]))/distance))
        return slope

    def __get_velocity(self, index):
        dist = self.atr_distances[index]
        time = 60 * self.atr_times[index]
        return (dist/time) * 3.6

    def __get_max_value_from_dict(self, key):
        values = []
        for i in range(len(self.__emissions_for_pollutant[key])):
            values.append(max(self.__emissions_for_pollutant[key][i]))
        return max(values)

    def calculate_emissions(self):
        all_roads_slopes = []
        all_roads_distances = []

        self.__init_emission_dict()

        for j in range(len(self.paths)):
            slopes = []
            distances = []
            for i in range(len(self.paths[j])):
                if (i + 1) < len(self.paths[j]):
                    if len(distances) > 0:
                        dist = distances[-1] + self.__get_distance_3d(self.paths[j][i], self.paths[j][i + 1]) / 1000
                        distances.append(dist)
                    else:
                        distances.append(self.__get_distance_3d(self.paths[j][i], self.paths[j][i + 1]) / 1000)
                    slopes.append(self.__get_slope(self.paths[j][i], self.paths[j][i + 1]))
            all_roads_slopes.append(slopes)
            all_roads_distances.append(distances)

        for j in range(len(all_roads_slopes)):
            self.emissionJson.velocity = self.__get_velocity(j)
            for i in range(len(all_roads_slopes[j])):
                self.emissionJson.slope = all_roads_slopes[j][i]
                for k in range(len(self.__pollutants)):
                    if self.__pollutants[k] in self.__emissions_for_pollutant:
                        calc_emission = self.emissionJson.get_emission_for_pollutant(self.__pollutants[k])
                        if len(self.__emissions_for_pollutant[self.__pollutants[k]][j]) > 0 and self.cumulative:
                            result_emission = self.__emissions_for_pollutant[self.__pollutants[k]][j][-1] + calc_emission
                        else:
                            result_emission = calc_emission
                        self.__emissions_for_pollutant[self.__pollutants[k]][j].append(result_emission)

        if self.show_in_graph:
            fig = plt.figure()
            figs = []
            pollutant_counter = 0
            for j in range(len(self.__pollutants)):
                if self.__pollutants[j] in self.__emissions_for_pollutant:
                    pollutant_counter +=1
                    num_plots = 100 * len(self.__emissions_for_pollutant) + 10 + pollutant_counter
                    ax = fig.add_subplot(num_plots)
                    ax.set_title(self.__pollutants[j])
                    ax.set_ylim(0, self.__get_max_value_from_dict(self.__pollutants[j]) + 1)
                    figs.append(ax)

            for i in range(len(self.paths)):
                pollutant_counter = 0
                self.statistics[i] = {}
                for j in range(len(self.__pollutants)):
                    if self.__pollutants[j] in self.__emissions_for_pollutant:
                        ax = figs[pollutant_counter]
                        ax.plot(all_roads_distances[i], self.__emissions_for_pollutant[self.__pollutants[j]][i])
                        pollutant_counter += 1
                        if self.cumulative:
                            self.statistics[i][self.__pollutants[j]] = max(self.__emissions_for_pollutant[self.__pollutants[j]][i])
                        else:
                            self.statistics[i][self.__pollutants[j]] = sum(self.__emissions_for_pollutant[self.__pollutants[j]][i])
            print self.statistics
            ax = figs[-1]
            labels = ["Route " + str(i+1) for i in range(len(self.paths))]
            pos = (len(figs)/10.0) * (-1)
            ax.legend(labels, loc=(0, pos), ncol = len(self.paths))
            plt.show()
        else:
            for i in range(len(self.paths)):
                self.statistics[i] = {}
                for j in range(len(self.__pollutants)):
                    if self.__pollutants[j] in self.__emissions_for_pollutant:
                        if self.cumulative:
                            self.statistics[i][self.__pollutants[j]] = max(self.__emissions_for_pollutant[self.__pollutants[j]][i])
                        else:
                            self.statistics[i][self.__pollutants[j]] = sum(self.__emissions_for_pollutant[self.__pollutants[j]][i])
            print self.statistics

if __name__ == "__main__":
    VERSION = "1.0"
    description = "Emission Calculator Lib"
    parser = OptionParser(usage="usage: % prog [options] start<startCoord>",
                          version="%prog " + VERSION + ", Copyright (c) TRAN",
                          description=description, add_help_option=True)

    parser.add_option("--start", dest="startCoord", default=[0,0], help='Set start coordinates', metavar="Array")
    parser.add_option("--end", dest="endCoord", default=[0,0], help='Set end coordinates', metavar="Array")
    parser.add_option("--length", dest="length", default=12, help='Vehicle length', metavar="Value")
    parser.add_option("--height", dest="height", default=4.5, help='Vehicle height', metavar="Value")
    parser.add_option("--load", dest="load", default=0, help="Vehicle load")
    parser.add_option("--input", dest="inputFile", default="", help='Set type vehicle motor, this is necessary for'
                                                                     ' calculate emission', metavar="String")
    parser.add_option("--nox", dest="nox", default=True, help='Get NOx emissions', metavar="Bool")
    parser.add_option("--co", dest="co", default=True, help='Get CO emissions', metavar="Bool")
    parser.add_option("--hc", dest="hc", default=True, help='Get HC emissions', metavar="Bool")
    parser.add_option("--pm", dest="pm", default=True, help='Get PM emissions', metavar="Bool")
    parser.add_option("--fc", dest="fc", default=True, help='Get FC emissions', metavar="Bool")
    parser.add_option("--cumulative", dest="cumulative", default=True, help='Cumulative curve in graph', metavar="Bool")
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
            print "Route " + str(i + 1)
            print "Length: " + str(distance) + " km, driving time: " + str(hours) + " hours and " + str(
                    minutes) + " minutes."
        if options.inputFile != "":
            emission_calculator.emissionJson.read_data_from_input_file(options.inputFile)
            emission_calculator.calculate_emissions()
