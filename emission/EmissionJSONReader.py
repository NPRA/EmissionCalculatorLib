import os
import json
import gzip
import math

from . import Interpolate
from . import Extrapolate
from . import vehicles
from . import log


class EmissionsJsonParser:
    def __init__(self, vehicle, pollutants, filename="roadTransport.json.gz"):
        self._filename = filename
        self._data = None
        self._parsed_data = {}
        self._vehicle = vehicle

        # TODO: Don't need this?
        self._slope = 0

        self._pollutants = pollutants

        self._read_data()
        self._parse_data()

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

    def get_modes(self):
        modes = set()
        categories = self._data.get("Type", None)
        for c in categories:
            cat_id = c.get("Id")
            vehicle_type = vehicles.Vehicle.get_type_for_category(cat_id)
            if vehicle_type != self._vehicle.type:
                continue

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

                        if self._vehicle.euro_std != es_id:
                            continue

                        modes = es.get("Mode")
                        for m in modes:
                            m_id = m.get("Id")
                            modes.add(m_id)
        return modes

    def _parse_data(self):
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
                    log.debug("subsegment_id: {}".format(subsegment_id))

                    euro_standard = s.get("TEC_NAME")
                    for es in euro_standard:
                        es_id = es.get("Id")

                        if self._vehicle.euro_std != es_id:
                            continue
                        log.debug("es_id: {}".format(es_id))
                        # continue

                        modes = es.get("Mode")
                        for m in modes:
                            m_id = m.get("Id")

                            if self._vehicle.mode != m_id:
                                continue
                            log.debug("mode_id: {}".format(m_id.encode("utf-8")))

                            slopes = m.get("Slope")
                            for s in slopes:
                                slope_id = s.get("Id")

                                #if self._vehicle.slope != slope_id:
                                #    continue
                                log.debug("slope_id: {}".format(slope_id.encode("utf-8")))

                                loads = s.get("Load")
                                for l in loads:
                                    l_id = l.get("Id")

                                    if self._vehicle.load > -1:
                                        if self._vehicle.load != float(l_id):
                                            continue
                                    log.debug("load id: ".format(l_id.encode("utf-8")))

                                    pollutants = l.get("Pollutant")
                                    for p in pollutants:
                                        p_id = p.get("Id")
                                        if p_id in self._pollutants:
                                            new_obj = {
                                                "category": cat_id,
                                                "subsegment": subsegment_id,
                                                "euro_standard": es_id,
                                                "slope": float(slope_id) if slope_id != "" else 0.0,
                                            }
                                            new_obj.update(p)

                                            if not self._pollutants.get(p_id, None):
                                                self._pollutants[p_id] = []
                                            self._pollutants[p_id].append(new_obj)

                                            # print("Pollutant: {}".format(p.get("Id")))
                                            # print("     new_obj: {}".format(new_obj))

    def get_for_pollutant(self, pollutant_id, slope=None):
        if pollutant_id not in self._pollutants:
            raise ValueError("Pollutant ID not in list of pollutations to search for..")

        log.debug("== POLLUTANT_ID = {}".format(pollutant_id))

        pollutant = None
        if len(self._pollutants[pollutant_id]) > 1:
            positive_slopes = [0, 0.02, 0.04, 0.06]
            negative_slopes = [-0.06, -0.04, -0.02, 0]

            # Multiple items in list, meaning we have 
            # various slope values
            x = [x for x in self._pollutants[pollutant_id] if x['slope'] == slope]
            if any(x):
                log.debug("FOUND MATCH: {}".format(slope))
                pollutant = x[0]
                log.debug("      pollutant: {}".format(pollutant))
            else:
                # No match was found. Need to Extrapolate / Interpolate the 
                # emission value
                log.debug("NO MATCH: {}".format(slope))
                slopes_for_pollutant = []
                if slope > 0.0:
                    tmp_pollutants = [x for x in self._pollutants[pollutant_id] if x['slope'] in positive_slopes]
                    slopes_for_pollutant = map(EmissionsJsonParser.calculate, tmp_pollutants)
                    extrapolate = Extrapolate(positive_slopes, slopes_for_pollutant)
                    tmp = extrapolate[slope]
                    log.debug("Extrapolated value: {}".format(tmp))
                    return tmp

                else:
                    tmp_pollutants = [x for x in self._pollutants[pollutant_id] if x['slope'] in negative_slopes]
                    slopes_for_pollutant = map(EmissionsJsonParser.calculate, tmp_pollutants)
                    interpolate = Interpolate(negative_slopes, slopes_for_pollutant)
                    tmp = interpolate[slope]
                    log.debug("Interpolated value: {}".format(tmp))
                    return tmp

        else:
            pollutant = self._pollutants[pollutant_id][0]
        tmp = EmissionsJsonParser.calculate(pollutant)
        log.debug("Regular value: {}".format(tmp))
        return tmp

    @staticmethod
    def calculate(pollutant):
        """
            this calculation is taken from the EU spreadsheet!
        """
        alpha = float(pollutant.get("Alpha"))
        beta = float(pollutant.get("Beta"))
        delta = float(pollutant.get("Delta"))
        epsilon = float(pollutant.get("Epsilon"))
        gamma = float(pollutant.get("Gamma"))
        hta = float(pollutant.get("Hta"))
        reduct_fact = float(pollutant.get("Reduction Factor [%]"))
        speed = float(pollutant.get("Speed"))
        v_max = float(pollutant.get("Vmax"))
        v_min = float(pollutant.get("Vmin"))
        zita = float(pollutant.get("Zita"))

        """ ((alpha*speed^2) + (beta*speed) + gamma + (delta/speed))/((epsilon*speed^2) * (zita * speed + htz))"""
        result = (alpha * math.pow(speed, 2)) + (beta * speed) + gamma + (delta / speed)
        result /= (epsilon * math.pow(speed, 2)) + ((zita * speed) + hta)
        result *= (1 - reduct_fact)
        return result
