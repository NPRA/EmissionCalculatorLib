import sys
import os

cwd = os.path.dirname(os.path.abspath(__file__))
cwd_parent = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(cwd)
sys.path.append(cwd_parent)

import emission


if __name__ == '__main__':
    calc = emission.EmissionCalculatorLib()
    calc.length
    calc.length = 124

    start_coord = [271809.847394, 7039133.17755]
    # end_coord = [287118.751014, 6746519.41028]
    end_coord = [265385.432115, 7031118.13344]

    vehicle_length = 12
    vehicle_height = 4.4
    vehicle_load = 1

    coordinates = "{start[0]},{start[1]};{end[0]},{end[1]}".format(
        start=start_coord, end=end_coord)
    print("coordinates: {}".format(coordinates))
    calc.coordinates = coordinates
    calc.length = vehicle_length
    calc.height = vehicle_height
    calc.load = vehicle_load

    calc.get_json_from_url()

    if calc.paths:
        print("Got returned paths: {}".format(len(calc.paths)))

        for i, r in enumerate(calc.atr_distances):
            distance = calc.atr_distances[i] / 1000
            hours, minutes = divmod(calc.atr_times[i], 60)
            hours = int(hours)
            minutes = int(minutes)
            print("Route {}".format(i + 1))
            print("Length: {} km, driving time: {}:{}".format(distance, hours, minutes))
    else:
        print("No returned paths..")

    print("Summary: {}".format(calc.emission_summary))
