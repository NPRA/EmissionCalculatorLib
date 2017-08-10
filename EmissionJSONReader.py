import json
from EquationGenerator import EquationGenerator


class EmissionsJsonReader:
    def __init__(self):
        self.type = ""
        self.ssc_name = ""
        self.subsegment = ""
        self.tec_name = ""
        self.slope = 0
        self.load = ""
        self.velocity = 0

        # Result from filter
        self.filtred_tec_name = []

        self.__load_input_data()
        self.__filter_input_to_tec_name()

    def __load_input_data(self):
        f = open("inputData.txt", "r")
        data = f.read().split(";")
        self.type = data[0]
        self.ssc_name = data[1]
        self.subsegment = data[2]
        self.tec_name = data[3]
        # self.slope = data[4]
        self.load = data[5]
        # self.velocity = int(data[6])

    def __filter_input_to_tec_name(self):
        with open("convertedData.json") as data_file:
            data = json.load(data_file)

        type = filter(lambda type: type["Name"] == self.type, data["Type"])
        ssc_name = filter(lambda sscName: sscName["Name"] == self.ssc_name, type[0]["SSC_NAME"])
        subsegment = filter(lambda subseg: subseg["Name"] == self.subsegment, ssc_name[0]["Subsegment"])
        self.filtred_tec_name = filter(lambda tecName: tecName["Name"] == self.tec_name, subsegment[0]["TEC_NAME"])


    def get_emission_for_pollutant(self, pollutant):
        # with open("convertedData.json") as data_file:
        #     data = json.load(data_file)
        #
        # type = filter(lambda type: type["Name"] == self.type, data["Type"])
        # ssc_name = filter(lambda sscName: sscName["Name"] == self.ssc_name, type[0]["SSC_NAME"])
        # subsegment = filter(lambda subseg: subseg["Name"] == self.subsegment, ssc_name[0]["Subsegment"])
        # tec_name = filter(lambda tecName: tecName["Name"] == self.tec_name, subsegment[0]["TEC_NAME"])
        slope = filter(lambda slope: slope["id"] == str(self.slope), self.filtred_tec_name[0]["Slope"])
        load = filter(lambda load: load["id"] == self.load, slope[0]["Load"])
        pollutant_data = filter(lambda load: load["id"] == pollutant, load[0]["Pollutant"])

        emission = EquationGenerator(pollutant_data[0], self.velocity).get_result()

        return emission

if __name__ == "__main__":
    EmissionsJsonReader()