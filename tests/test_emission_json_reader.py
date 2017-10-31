from emission import EmissionsJsonParser
from emission import vehicles, PollutantTypes


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class TestEmissionsJsonParser:
    def test_init(self):
        fuel_type = vehicles.FuelTypes.PETROL
        vehicle = vehicles.Car(fuel_type)
        pollutants = {
            PollutantTypes.CO: None,
            PollutantTypes.PM_EXHAUST: None
        }

        ejp = EmissionsJsonParser(vehicle, pollutants)
        assert ejp is not None

    def test_calculate(self):
        pollutant = {
            "Alpha": 0.00000000000549670697736844,
            "Beta": -0.0334176120766537,
            "Delta": -0.000000104372710338195,
            "Epsilon": 0.00187153627565408,
            "Gamma": 5.10983452219724,
            "Hta": 37.5057390279501,
            "Reduction Factor [%]": 0,
            "Zita": -0.52883090616296,
            "Speed": 100,
            "Vmax": 44,
            "Vmin": 0,
        }

        expected_result = 0.529678
        result = EmissionsJsonParser.calculate(pollutant)
        assert isclose(result, expected_result, rel_tol=1e-03)
