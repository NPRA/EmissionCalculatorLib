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
    # fuel_diesel = emission.vehicles.FuelTypes.BIO_DIESEL
    vehicle = emission.vehicles.Truck(fuel_diesel)

    planner = emission.Planner(start, stop, vehicle)
    planner.add_pollutant(emission.PollutantTypes.NOx)
    planner.add_pollutant(emission.PollutantTypes.CO)

    try:
        planner.run()
    except emission.exceptions.RouteError as err:
        print("error: {}".format(err))
        print("Unable to get a good response from web service")
        sys.exit(1)

    routes = planner.routes

    print("Pollutants: {}".format(planner.pollutants.keys()))
    pollutant_types = planner.pollutants.keys()
    for r in routes:
        print("Route: {}".format(r))
        for pt in pollutant_types:
            print("    {} = {}".format(pt, r.total_emission(pt)))

    print("\nTesting below....:")

    routes.sort()
    print("After sorted..:")
    for r in routes:
        print(">> {}".format(r))

    sorted_after_NOx = sorted(routes, key=lambda x: x.total_emission('NOx'))
    print("Sorted after NOx..:")
    for r in sorted_after_NOx:
        print(">> {} NOx: {}".format(r, r.total_emission('NOx')))

    sorted_after_CO = sorted(routes, key=lambda x: x.total_emission('CO'))
    print("Sorted after CO")
    for r in sorted_after_CO:
        print(">> {} CO: {}".format(r, r.total_emission('CO')))
