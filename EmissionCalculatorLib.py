import math
import json
try:
    from urllib.request import urlopen  # Python 3
except ImportError:
    from urllib import urlopen  # Python 2
from EmissionJSONReader import EmissionsJsonReader
import matplotlib.pyplot as plt


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
        # self.vehicle_load = "50"
        # self.vehicle_load = self.emissionJson.load
        # private values
        self.__pollutants = ["NOx", "CO", "HC", "PM", "FC"]
        self.__emissions_for_pollutant = {}

        # temp values
        self.__atributes = {}
        self.__atr_distances = []
        self.__atr_times = []

    def __init_emission_dict(self):
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

    def get_json_from_url(self):
        load = self.emissionJson.load
        # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=270337.81,7041814.57%3B296378.67,7044118.5&weight=50&geometryformat=isoz"
        url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops="+self.coordinates+"&weight="+load+"&geometryformat=isoz"
        # url with 3 roads from Oslo to Molde
        # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=262210.96,6649335.15%3B96311.150622257,6969883.5407672&weight=50&geometryformat=isoz"
        response = urlopen(url)
        data = json.loads(response.read())

        for i in range(len(data["routes"]["features"])):
            self.__atr_distances.append(data["routes"]["features"][i]['attributes']["Total_Meters"])
            self.__atr_times.append(data["routes"]["features"][i]['attributes']["Total_Minutes"])
            self.paths.append(data["routes"]["features"][i]["geometry"]["paths"][0])

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
        dist = self.__atr_distances[index]
        time = 60 * self.__atr_times[index]
        return (dist/time) * 3.6

    def __get_max_value_from_dict(self, key):
        values = []
        for i in range(len(self.__emissions_for_pollutant[key])):
            values.append(max(self.__emissions_for_pollutant[key][i]))
        return max(values)

    def calculate_emissions(self):
        all_slopes = []
        all_distances = []

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
            all_slopes.append(slopes)
            all_distances.append(distances)

        for j in range(len(all_slopes)):
            self.emissionJson.velocity = self.__get_velocity(j)
            for i in range(len(all_slopes[j])):
                self.emissionJson.slope = all_slopes[j][i]
                for k in range(len(self.__pollutants)):
                    if self.__pollutants[k] in self.__emissions_for_pollutant:
                        calc_emission = self.emissionJson.get_emission_for_pollutant(self.__pollutants[k])
                        if len(self.__emissions_for_pollutant[self.__pollutants[k]][j]) > 0 and self.cumulative:
                            result_emission = self.__emissions_for_pollutant[self.__pollutants[k]][j][-1] + calc_emission
                        else:
                            result_emission = calc_emission
                        self.__emissions_for_pollutant[self.__pollutants[k]][j].append(result_emission)

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
            for j in range(len(self.__pollutants)):
                if self.__pollutants[j] in self.__emissions_for_pollutant:
                    ax = figs[pollutant_counter]
                    ax.plot(all_distances[i], self.__emissions_for_pollutant[self.__pollutants[j]][i])
                    pollutant_counter += 1

        plt.show()

if __name__ == "__main__":
    a = EmissionCalculatorLib()
    a.get_json_from_url()
    a.calculate_emissions()