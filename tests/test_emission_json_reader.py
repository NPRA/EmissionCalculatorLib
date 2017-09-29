from emission import EmissionsJsonReader, EmissionsJsonParser
from emission import vehicles


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