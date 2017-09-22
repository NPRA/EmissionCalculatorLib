def enum(**named_values):
    return type('Enum', (), named_values)


VehicleTypes = enum(CAR='car', BUS='bus', TRUCK='truck')


class Vehicle(object):
    def __init__(self, vtype, length=0, height=0, load=0):
        self.type = vtype
        self.length = length
        self.height = height
        self.load = load


class Car(Vehicle):
    def __init__(self):
        super(Car, self).__init__(VehicleTypes.CAR)


class Bus(Vehicle):
    def __init__(self):
        super(Bus, self).__init__(VehicleTypes.BUS)


class Truck(Vehicle):
    def __init__(self, length, height, load=1):
        super(Truck, self).__init__(VehicleTypes.TRUCK, length, height, load)
