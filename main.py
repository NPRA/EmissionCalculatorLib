import math
import urllib, json
from EmissionJSONReader import EmissionsJsonReader
import matplotlib.pyplot as plt


class EmissionCalculatorLib:
    def __init__(self):
        #init values
        self.jsonData = {}
        self.distances = []
        self.emissions = []

        #start calculation
        self.get_json_from_url()
        self.calculate_distance()

    def get_json_from_url(self):
        url = "http://multirit.triona.se/routingService_v1_0/routingService?barriers=&format=json&height=4.5&lang=nb-no&length=12&stops=270337.81,7041814.57%3B296378.67,7044118.5&weight=50&geometryformat=isoz"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        self.jsonData = data["routes"]["features"][0]["geometry"]["paths"][0]
        print self.jsonData

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
            slope = math.degrees(math.asin((point2[2]- point1[2])/distance))
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

    def calculate_distance(self):
        temp_values = []
        slopes = []
        for i in range(len(self.jsonData)):
            # if (i < 10):
                if (i + 1) < len(self.jsonData):
                    if len(self.distances) > 0:
                        dist = self.distances[-1] + self.get_distance_3d(self.jsonData[i], self.jsonData[i + 1]) / 1000
                        self.distances.append(dist)
                    else:
                        self.distances.append(self.get_distance_3d(self.jsonData[i], self.jsonData[i + 1]) / 1000)

                    slopes.append(int(round(self.get_slope(self.jsonData[i], self.jsonData[i + 1]))))
            # else:
            #     break
                # temp_values.append(i)
        emission = EmissionsJsonReader()
        emission.velocity = 58

        for i in range(len(slopes)):
            # if (i < 10):
                emission.slope = self.get_fake_slope(slopes[i])
                temp_values.append(emission.get_emission_for_pollutant("NOx"))
            # else:
            #     break
        # print temp_values

        plt.plot(self.distances, temp_values)
        plt.axis([0, self.distances[-1]+1, 0, max(temp_values)+1])
        plt.show()

if __name__ == "__main__":
    EmissionCalculatorLib()