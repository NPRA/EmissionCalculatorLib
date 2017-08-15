import math
import urllib, json
from EmissionJSONReader import EmissionsJsonReader
import matplotlib.pyplot as plt


class EmissionCalculatorLib:
    def __init__(self):
        #init values
        self.jsonData = {}
        # self.distances = []
        self.emissions = []

        #temp values
        self.atributes = {}
        self.atr_distances = []
        self.atr_times = []
        self.paths = []


        #start calculation
        self.get_json_from_url()
        self.calculate_distance()

    def get_json_from_url(self):
        url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=270337.81,7041814.57%3B296378.67,7044118.5&weight=50&geometryformat=isoz"
        # url with 3 roads from Oslo to Molde
        # url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=262210.96,6649335.15%3B96311.150622257,6969883.5407672&weight=50&geometryformat=isoz"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        # fix here data["routes"]["features"] - if more roads are available
        for i in range(len(data["routes"]["features"])):
            self.atr_distances.append(data["routes"]["features"][i]['attributes']["Total_Meters"])
            self.atr_times.append(data["routes"]["features"][i]['attributes']["Total_Minutes"])
            self.paths.append(data["routes"]["features"][i]["geometry"]["paths"][0])

        self.jsonData = data["routes"]["features"][0]["geometry"]["paths"][0]
        # print self.jsonData

    @staticmethod
    def get_distance_2d(point1, point2):
        distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return distance

    @staticmethod
    def get_distance_3d(point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)
        return distance

    def get_slope(self, point1, point2):
        distance = self.get_distance_3d(point1, point2)
        slope = 0.0
        if distance != 0:
            slope = math.degrees(math.asin((float(point2[2])- float(point1[2]))/distance))
        # print slope, point2, point1, distance
        return slope

    @staticmethod
    def get_fake_slope(slope):
        if slope > 6:
            return 6
        elif slope < -6:
            return -6
        else:
            slope_dict = {0: 0, 1: 0, 2: 2, 3: 2, 4: 4, 5: 4, 6: 6, -1: 0, -2: -2, -3: -2, -4: -4, -5: -4, -6: -6}
            return slope_dict[slope]

    def get_velocity(self, index):
        dist = self.atr_distances[index]
        time = 60 * self.atr_times[index]
        return (dist/time) * 3.6

    def calculate_distance(self):
        all_nox_values = []
        all_slopes = []
        all_distances = []

        for j in range(len(self.paths)):
            slopes = []
            distances = []
            for i in range(len(self.paths[j])):
                if (i + 1) < len(self.paths[j]):
                    if len(distances) > 0:
                        dist = distances[-1] + self.get_distance_3d(self.jsonData[i], self.jsonData[i + 1]) / 1000
                        distances.append(dist)
                    else:
                        distances.append(self.get_distance_3d(self.jsonData[i], self.jsonData[i + 1]) / 1000)
                    slopes.append(self.get_slope(self.paths[j][i], self.paths[j][i + 1]))
            all_slopes.append(slopes)
            all_distances.append(distances)

        for j in range(len(all_slopes)):
            nox_values = []
            emission = EmissionsJsonReader()
            emission.velocity = self.get_velocity(j)
            for i in range(len(all_slopes[j])):
                emission.slope = all_slopes[j][i]
                nox_values.append(emission.get_emission_for_pollutant("NOx"))
            all_nox_values.append(nox_values)

        max_y_emissions = []

        for i in range(len(all_nox_values)):
            plt.plot(all_distances[i], all_nox_values[i])
            max_y_emissions.append(max(all_nox_values[i]))
        # plt.plot(temp_values)

        plt.axis([0, max(self.atr_distances)/1000, 0, max(max_y_emissions)+1])
        plt.show()

if __name__ == "__main__":
    EmissionCalculatorLib()