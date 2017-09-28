def enum(**named_values):
    return type('Enum', (), named_values)


VehicleTypes = enum(CAR='car', BUS='bus', TRUCK='truck', LCATEGORY='L-category', VAN='van')
FuelTypes = enum(PETROL='Petrol',
                 DIESEL='Diesel',
                 PETR_HYB='Petrol Hybrid',
                 LPG_BIFUEL_LPG='LPG Bifuel ~ LPG',
                 LPG_BIFUEL_PETROL='LPG Bifuel ~ Petrol',
                 CNG_BIFUEL_CNG='CNG Bifuel ~ CNG',
                 CNG_BIFUEL_PETROL='CNG Bifuel ~ Petrol',
                 CNG='CNG',
                 BIO_DIESEL='Biodiesel')


class Vehicle(object):
    def __init__(self, vtype, fuel_type, length=0, height=0, load=0):
        self.type = vtype
        self.fuel_type = fuel_type
        self.length = length
        self.height = height
        self.load = load


    @staticmethod
    def get_type_for_category(category_id):
        mapping = {
            'Passenger Cars': VehicleTypes.CAR,
            'Light Commercial Vehicles': VehicleTypes.VAN,
            'Heavy Duty Trucks': VehicleTypes.TRUCK,
            'Buses': VehicleTypes.BUS,
            'L-Category': VehicleTypes.LCATEGORY
        }
        return mapping.get(category_id, None)


class LCategory(Vehicle):
    """Scooters, 2 and 3-wheels
    """
    def __init__(self, fuel_type):
        super(LCategory, self).__init__(VehicleTypes.LCategory, fuel_type)


class Car(Vehicle):
    """Regular passenger car"""
    def __init__(self, fuel_type):
        super(Car, self).__init__(VehicleTypes.CAR, fuel_type)


class Van(Vehicle):
    """Light Commercial Car"""
    def __init__(self, fuel_type):
        super(Van, self).__init__(VehicleTypes.VAN, fuel_type)


class Bus(Vehicle):
    """Buses"""
    def __init__(self, fuel_type):
        super(Bus, self).__init__(VehicleTypes.BUS, fuel_type)


class Truck(Vehicle):
    """Heavy Duty Trucks"""
    def __init__(self, fuel_type, length, height, load=1):
        super(Truck, self).__init__(VehicleTypes.TRUCK, fuel_type, length, height, load)
