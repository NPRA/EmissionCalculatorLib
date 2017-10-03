import sys
import os

cwd = os.path.dirname(os.path.abspath(__file__))
cwd_parent = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(cwd)
sys.path.append(cwd_parent)


import emission


if __name__ == '__main__':
    start = [271809.847394, 7039133.17755]
    stop = [265385.432115, 7031118.13344]
    # fuel_petrol = emission.vehicles.FuelTypes.PETROL
    # vehicle = emission.vehicles.Car(fuel_petrol)
    fuel_diesel = emission.vehicles.FuelTypes.DIESEL
    vehicle = emission.vehicles.Truck(fuel_diesel)


    planner = emission.Planner(start, stop, vehicle)
    planner.add_pollutant(emission.PollutantTypes.NOx)
    planner.add_pollutant(emission.PollutantTypes.CO)
    planner.run()
