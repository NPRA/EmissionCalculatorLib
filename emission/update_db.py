import os
import json
import gzip
import sqlalchemy
from sqlalchemy.sql.expression import ClauseElement
import operator

from . import models


class Parser:
    def __init__(self, filename="roadTransport.json.gz"):
        self._data = self.readData(filename)
        self._parameters = []

    def readData(self, filename):
        gzip_json = os.path.join(os.path.dirname(__file__), filename)
        if os.path.isfile(gzip_json):
            with gzip.open(gzip_json, "rt") as data_file:
                return json.loads(data_file.read())
        else:
            raise IOError("Can't find file {}".format(filename))

    def _exists(self, model, name, p_name):
        return models.session.query(name(model)).filter_by(name=p_name).scalar() is not None

    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            instance = model(**params)
            session.add(instance)
            return instance, True

    def add(self, parm):
        s = models.session

        # import pdb; pdb.set_trace()
        category, _ = Parser.get_or_create(s, models.Category, name=parm.get("cat"))
        fuel, _ = Parser.get_or_create(s, models.Fuel, name=parm.get("fuel"))
        segment, _ = Parser.get_or_create(s, models.Segment, name=parm.get("segment"))
        eurostd, _ = Parser.get_or_create(s, models.EuroStd, name=parm.get("eurostd"))
        mode, _ = Parser.get_or_create(s, models.Mode, name=parm.get("mode"))
        pollutant, _ = Parser.get_or_create(s, models.Pollutant, name=parm.get("pollutant"))

        # Create parameter instance
        parm_parms = parm.get("parameters")
        parameter = models.Parameter(
            ALPHA=parm_parms.get("Alpha"),
            BETA=parm_parms.get("Beta"),
            DELTA=parm_parms.get("Delta"),
            EPSILON=parm_parms.get("Epsilon"),
            GAMMA=parm_parms.get("Gamma"),
            HTA=parm_parms.get("Hta"),
            MAXSPEED=parm_parms.get("Vmax"),
            MINSPEED=parm_parms.get("Vmin"),
            REDUCTIONFACTOR=parm_parms.get("Reduction Factor [%]"),
            SPEED=parm_parms.get("Speed"),
            ZITA=parm_parms.get("Zita"),
            slope=parm.get("slope"),
            load=parm.get("load"))
        parameter.category = category

        parameter.fuel = fuel
        parameter.segment = segment
        parameter.eurostd = eurostd
        parameter.mode = mode
        parameter.pollutant = pollutant

        # temp store for bulk insertion later
        self._parameters.append(parameter)

    def _parse_data(self):
        if not self._data:
            raise ValueError("No data to parse.. Something went wrong trying to read input data..")

        categories = self._data.get("Type", None)
        if not categories:
            raise AttributeError("Missing 'Type' in JSON file. Inspect file!")

        for c in categories:
            cat_id = c.get("Id")

            fuel = c.get("SSC_NAME")
            for f in fuel:
                fuel_id = f.get("Id")

                subsegments = f.get("Subsegment")
                for s in subsegments:
                    subsegment_id = s.get("Id")

                    euro_standard = s.get("TEC_NAME")
                    for es in euro_standard:
                        es_id = es.get("Id")

                        modes = es.get("Mode")
                        for m in modes:
                            m_id = m.get("Id")

                            slopes = m.get("Slope")
                            for s in slopes:
                                slope_id = s.get("Id")

                                loads = s.get("Load")
                                for l in loads:
                                    l_id = l.get("Id")

                                    pollutants = l.get("Pollutant")
                                    for p in pollutants:
                                        p_id = p.get("Id")

                                        parm = {
                                            "cat": cat_id,
                                            "fuel": fuel_id,
                                            "segment": subsegment_id,
                                            "eurostd": es_id,
                                            "mode": m_id,
                                            "pollutant": p_id,
                                            "slope": slope_id,
                                            "load": l_id,
                                            "parameters": p
                                        }
                                        self.add(parm)

        print("bulk inserting {} parameters".format(len(self._parameters)))
        models.session.add_all(self._parameters)
        models.session.flush()
        models.session.commit()
        print("Done!")
