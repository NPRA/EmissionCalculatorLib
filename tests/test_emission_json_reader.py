from emission import EmissionsJsonReader, EmissionsJsonParser
from emission import vehicles


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class TestEmissionJsonReader:
    def test_construct(self):
        fuel_type = vehicles.FuelTypes.PETROL
        vehicle = vehicles.Car(fuel_type)
        ejr = EmissionsJsonReader()
        assert ejr is not None

    def test_init_with_data(self):
        #ejr = EmissionsJsonReader()
        #ejr._init_values_from_input_file()
        #assert len(ejr._result_mode) > 0
        fuel_type = vehicles.FuelTypes.PETROL
        vehicle = vehicles.Car(fuel_type)
        ejp = EmissionsJsonParser(vehicle)
        assert ejp is not None

    def test_calculate(self):
        alpha = 0.00000000000549670697736844
        beta = -0.0334176120766537
        delta = -0.000000104372710338195
        epsilon = 0.00187153627565408
        gamma = 5.10983452219724
        hta = 37.5057390279501
        reduct_fact = 0
        zita = -0.52883090616296
        speed = 44

        expected_result = 0.2038
        result = EmissionsJsonParser.calculate(alpha, beta, delta, epsilon,
                                               gamma, hta, reduct_fact,
                                               zita, speed)
        assert isclose(result, expected_result, rel_tol=1e-03)
