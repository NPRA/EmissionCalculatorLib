import os
import json
import sys
import gzip
import math

# from . import EquationGenerator
from . import Interpolate
from . import Extrapolate
from . import vehicles


class EmissionsJsonParser:
    def __init__(self, vehicle, filename="roadTransport.json.gz"):
        self._filename = filename
        self._data = None
        self._parsed_data = {}
        self._vehicle = vehicle

        # TODO: Don't need this?
        self._slope = 0

        self._read_data()
        # self._parse_data()

    def _read_data(self):
        gzip_json = os.path.join(os.path.dirname(__file__), self._filename)
        if os.path.isfile(gzip_json):
            with gzip.open(gzip_json, "rb") as data_file:
                self._data = json.loads(data_file.read())
        else:
            raise IOError("Can't find file {}".format(self._filename))

    @staticmethod
    def get_fuel_type(fuel_id):
        for k, v in vehicles.FuelTypes.__dict__.items():
            if v == fuel_id:
                return v
        return None

    def get_subsegments(self):
        """Util method to list all subsegments for the vehicle
        passed when constructing this object
        """
        subsegments = set()

        categories = self._data.get("Type", None)
        if not categories:
            raise AttributeError("Missing 'Type' in JSON file. Inspect file!")

        for c in categories:
            cat_id = c.get("Id")
            vehicle_type = vehicles.Vehicle.get_type_for_category(cat_id)
            if vehicle_type != self._vehicle.type:
                continue
            # print("cat_id: {}".format(cat_id))

            fuel = c.get("SSC_NAME")
            for f in fuel:
                fuel_id = f.get("Id")
                fuel_type = EmissionsJsonParser.get_fuel_type(fuel_id)

                if not fuel_type:
                    raise ValueError("BAD FUEL TYPE!")

                if fuel_type != self._vehicle.fuel_type:
                    continue

                subsegments = f.get("Subsegment")
                for s in subsegments:
                    subsegment_id = s.get("Id").encode("utf-8")
                    subsegments.add(subsegment_id)
        return subsegments

    def get_euro_standards(self):
        """Util method to list all euro standards for the vehicle
        passed when constructing this object
        """
        euro_standards = set()

        categories = self._data.get("Type", None)
        for c in categories:
            cat_id = c.get("Id")
            vehicle_type = vehicles.Vehicle.get_type_for_category(cat_id)
            if vehicle_type != self._vehicle.type:
                continue
            # print("cat_id: {}".format(cat_id))

            fuel = c.get("SSC_NAME")
            for f in fuel:
                fuel_id = f.get("Id")
                fuel_type = EmissionsJsonParser.get_fuel_type(fuel_id)

                if not fuel_type:
                    raise ValueError("BAD FUEL TYPE!")

                if fuel_type != self._vehicle.fuel_type:
                    continue

                subsegments = f.get("Subsegment")
                for s in subsegments:
                    subsegment_id = s.get("Id").encode("utf-8")

                    if self._vehicle.segment != subsegment_id:
                        continue

                    euro_standard = s.get("TEC_NAME")
                    for es in euro_standard:
                        es_id = es.get("Id")
                        euro_standards.add(es_id)
        return euro_standards


    def _parse_data(self, pollutants):
        if not self._data:
            raise ValueError("No data to parse.. Something went wrong trying to read input data..")

        categories = self._data.get("Type", None)
        if not categories:
            raise AttributeError("Missing 'Type' in JSON file. Inspect file!")

        mapping = {
            vehicles.VehicleTypes.CAR: vehicles.Car,
            vehicles.VehicleTypes.VAN: vehicles.Van,
            vehicles.VehicleTypes.BUS: vehicles.Bus,
            vehicles.VehicleTypes.LCATEGORY: vehicles.LCategory,
            vehicles.VehicleTypes.TRUCK: vehicles.Truck
        }

        # TODO: Refactore - this was primarily done for testing the JSON structure
        for c in categories:
            cat_id = c.get("Id")
            vehicle_type = vehicles.Vehicle.get_type_for_category(cat_id)
            if vehicle_type != self._vehicle.type:
                continue
            # print("cat_id: {}".format(cat_id))

            fuel = c.get("SSC_NAME")
            for f in fuel:
                fuel_id = f.get("Id")
                fuel_type = EmissionsJsonParser.get_fuel_type(fuel_id)

                if not fuel_type:
                    raise ValueError("BAD FUEL TYPE!")

                if fuel_type != self._vehicle.fuel_type:
                    continue

                subsegments = f.get("Subsegment")
                for s in subsegments:
                    subsegment_id = s.get("Id").encode("utf-8")

                    if self._vehicle.segment != subsegment_id:
                        continue
                    print("subsegment_id: {}".format(subsegment_id))

                    euro_standard = s.get("TEC_NAME")
                    for es in euro_standard:
                        es_id = es.get("Id")

                        if self._vehicle.euro_std != es_id:
                            continue
                        print("es_id: {}".format(es_id))
                        # continue

                        modes = es.get("Mode")
                        for m in modes:
                            m_id = m.get("Id")

                            if self._vehicle.mode != m_id:
                                continue
                            print("mode_id: {}".format(m_id.encode("utf-8")))

                            slopes = m.get("Slope")
                            for s in slopes:
                                slope_id = s.get("Id")

                                if self._vehicle.slope != slope_id:
                                    continue
                                print("slope_id: {}".format(slope_id.encode("utf-8")))

                                loads = s.get("Load")
                                for l in loads:
                                    l_id = l.get("Id")

                                    if self._vehicle.load > -1:
                                        if self._vehicle.load != float(l_id):
                                            continue
                                    print("load id: ".format(l_id.encode("utf-8")))

                                    pollutants = l.get("Pollutant")
                                    for p in pollutants:
                                        print("Pollutant: {}".format(p.get("Id")))
                                        # print("     subsegment: {}".format(subsegment_id))
                                        # print("     euro_standard: {}".format(es_id))
                                        # print("     mode: {}".format(m_id))
                                        # print("     slope: {}\n".format(slope_id))

                                        # TODO: Store each "pollutant" with meta-data such as
                                        #       category, fuel, subsegment, euro_standard, slope, load
                                        #
                                        #       but, use pollutant "Id" as dict key.
                                        new_obj = {
                                            "category": cat_id,
                                            "subsegment": subsegment_id,
                                            "euro_standard": es_id
                                        }
                                        new_obj.update(p)
                                        print("     new_obj: {}".format(new_obj))
                                        # self._add_pollutant(p.get("Id"), new_obj)

                                    # return

    def _add_pollutant(self, key, new_obj):
        pass

    def get_for_pollutant(self, pollutants):
        return 0.5

    @staticmethod
    def calculate(alpha, beta, delta, epsilon, gamma, hta, reduct_fact, zita, speed=44.0):
        """
            {
            "Alpha": "0.00000000000549670697736844",
            "Beta": "-0.0334176120766537",
            "Delta": "-0.000000104372710338195",
            "Epsilon": "0.00187153627565408",
            "Gamma": "5.10983452219724",
            "Hta": "37.5057390279501",
            "Id": "CO",
            "Reduction Factor [%]": "0",
            "Speed": "44",
            "Vmax": "130",
            "Vmin": "5",
            "Zita": "-0.52883090616296"
        },

            this calculation is taken from the EU spreadsheet!
        """

        """ ((alpha*speed^2) + (beta*speed) + gamma + (delta/speed))/((epsilon*speed^2) * (zita * speed + htz))"""
        result = (alpha * math.pow(speed, 2)) + (beta * speed) + gamma + (delta / speed)
        result /= (epsilon * math.pow(speed, 2)) + ((zita * speed) + hta)
        result *= (1 - reduct_fact)
        return result


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

        # TODO: Refactore this calculation - cleancode
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