from emission import Planner
from emission import PollutantTypes
from emission import vehicles


class TestPlanner:
    def test_construct(self):
        start = [271809.847394, 7039133.17755]
        stop = [265385.432115, 7031118.13344]
        vehicle = vehicles.Car(vehicles.FuelTypes.PETROL)

        planner = Planner(start, stop, vehicle)
        assert planner.pollutants == {}

        planner.add_pollutant(PollutantTypes.NOx)
        assert len(planner.pollutants) > 0
