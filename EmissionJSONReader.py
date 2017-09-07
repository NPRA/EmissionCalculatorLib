import os
import json
from EquationGenerator import EquationGenerator
from Interpolate import Interpolate
from Extrapolate import Extrapolate
import sys
import gzip


class EmissionsJsonReader:
    def __init__(self):
        # public values
        self.type = ""
        self.ssc_name = ""
        self.subsegment = ""
        self.tec_name = ""
        self.slope = 0
        self.load = "0"
        self.velocity = 0
        self.data = {}

        # private values
        self._result_type = []
        self._result_ssc = []
        self._result_subsegment = []
        # self._result_tec = []
        self._result_mode = []
        # self.read_data_from_input_file("inputData.txt")

    @staticmethod
    def _read_json_file():
        gzip_json = os.path.join(os.path.dirname(__file__), 'roadTransport.json.gz')
        if os.path.isfile(gzip_json):
            with gzip.open(gzip_json, "rb") as data_file:
                data = json.loads(data_file.read().decode("ascii"))
            return data
        else:
            sys.exit("Json file doesn't exist.")

    def set_type(self, value):
        self.type = value
        self._result_type = list(filter(lambda type: type["Id"] == self.type, self.data["Type"]))

    def set_ssc_name(self, value):
        self.ssc_name = value
        if len(self._result_type) > 0:
            self._result_ssc = list(filter(lambda sscName: sscName["Id"] == self.ssc_name, self._result_type[0]["SSC_NAME"]))

    def set_subsegment(self, value):
        self.subsegment = value
        if len(self._result_ssc):
            self._result_subsegment = list(filter(lambda subseg: subseg["Id"] == self.subsegment, self._result_ssc[0]["Subsegment"]))

    def set_tec_name(self, value):
        self.tec_name = value
        if len(self._result_subsegment):
            self._result_tec = list(filter(lambda tecName: tecName["Id"] == self.tec_name, self._result_subsegment[0]["TEC_NAME"]))

    def set_load(self, value):
        self.load = value

    def get_types(self):
        self.data = self._read_json_file()
        types = []
        for i in range(len(self.data["Type"])):
            types.append(self.data["Type"][i]["Id"])
        return types

    def get_ssc_names(self):
        ssc_names = []
        if len(self._result_type) > 0:
            for i in range(len(self._result_type[0]['SSC_NAME'])):
                ssc_names.append(self._result_type[0]['SSC_NAME'][i]["Id"])
        return ssc_names

    def get_subsegment(self):
        subsegments = []
        if len(self._result_ssc) > 0:
            for i in range(len(self._result_ssc[0]['Subsegment'])):
                subsegments.append(self._result_ssc[0]['Subsegment'][i]["Id"])
        return subsegments

    def get_tec_names(self):
        tec_names = []
        if len(self._result_subsegment) > 0:
            for i in range(len(self._result_subsegment[0]['TEC_NAME'])):
                tec_names.append(self._result_subsegment[0]['TEC_NAME'][i]["Id"])
        return tec_names

    def read_data_from_input_file(self, input_file):
        input_data = os.path.join(os.path.dirname(__file__), input_file)
        if os.path.isfile(input_data):
            f = open(input_data, "r")
            data = f.read().split(";")
            if len(data) < 4:
                sys.exit("Wrong input parameters!")
            self.type = data[0]
            self.ssc_name = data[1]
            self.subsegment = data[2]
            self.tec_name = data[3]
            self.mode = data[4]
            self._init_values_from_input_file()
        else:
            sys.exit("Invalid input file")

    def _init_values_from_input_file(self):

        # gzip_json = os.path.join(os.path.dirname(__file__), 'trucksEmissions.json.gz')
        # if os.path.isfile(gzip_json):
        #     with gzip.open(gzip_json, "rb") as data_file:
        #         data = json.loads(data_file.read().decode("ascii"))
        data = self._read_json_file()
        type = list(filter(lambda type: type["Id"] == self.type, data["Type"]))
        if len(type) > 0:
            ssc_name = list(filter(lambda sscName: sscName["Id"] == self.ssc_name, type[0]["SSC_NAME"]))
            if len(ssc_name) > 0:
                subsegment = list(filter(lambda subseg: subseg["Id"] == self.subsegment, ssc_name[0]["Subsegment"]))
                if len(subsegment) > 0 :
                    tec_name = list(filter(lambda tecName: tecName["Id"] == self.tec_name, subsegment[0]["TEC_NAME"]))
                    if len(tec_name) > 0:
                        self._result_mode = list(filter(lambda mode: mode["Id"] == self.mode, tec_name[0]["Mode"]))
        if not len(self._result_mode) > 0:
            sys.exit("Wrong input parameters!")
        # else:
        #     sys.exit("Json file doesn't exist.")

    def _calculate_emission_for_pollutant_by_slope(self, pollutant_value, slope_value):
        slope = list(filter(lambda slope: slope["Id"] == str(slope_value), self._result_mode[0]["Slope"]))
        if len(slope) == 0:
            return 0
        load = list(filter(lambda load: load["Id"] == self.load, slope[0]["Load"]))
        if len(load) == 0:
            return 0
        data = list(filter(lambda pollutant: pollutant["Id"] == pollutant_value, load[0]["Pollutant"]))[0]
        if len(data) == 0:
            return 0
        # emission = EquationGenerator(pollutant_data[0], self.velocity)
        # self.velocity = 44
        emission = (float(data['Alpha']) * self.velocity ** 2 + float(data['Beta']) * self.velocity + float(data['Gamma']) + (float(data['Delta']) / self.velocity)) / (float(data['Epsilon']) * self.velocity ** 2 + float(data['Zita']) * self.velocity + float(data['Hta'])) * (1 - float(data['Reduction Factor [%]']))
        return emission

    def get_emission_for_pollutant(self, pollutant):
        positive_slopes = [0, 0.02, 0.04, 0.06]
        negative_slopes = [-0.06, -0.04, -0.02, 0]
        if self.slope in positive_slopes or self.slope in negative_slopes:
            return self._calculate_emission_for_pollutant_by_slope(pollutant, int(self.slope))
        else:
            # for each slope - positive/negative calculate value - array will be use for Extrapolation/Interpolation
            # defined slope
            slopes_for_polutant = []
            if self.slope > 0.0:
                for i in range(len(positive_slopes)):
                    slopes_for_polutant.append(self._calculate_emission_for_pollutant_by_slope(pollutant, positive_slopes[i]))
                i = Extrapolate(positive_slopes, slopes_for_polutant)
                return i[self.slope]
            else:
                for i in range(len(negative_slopes)):
                    slopes_for_polutant.append(self._calculate_emission_for_pollutant_by_slope(pollutant, negative_slopes[i]))
                i = Interpolate(negative_slopes, slopes_for_polutant)
                return i[self.slope]