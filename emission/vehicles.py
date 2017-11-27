import six

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
    """Base class for all vehicle types
    """

    mapping = {
        'Passenger Cars': VehicleTypes.CAR,
        'Light Commercial Vehicles': VehicleTypes.VAN,
        'Heavy Duty Trucks': VehicleTypes.TRUCK,
        'Buses': VehicleTypes.BUS,
        'L-Category': VehicleTypes.LCATEGORY
    }

    def __init__(self, vtype, fuel_type, segment, euro_std, mode='', load=-1.0, height=2.0, length=5.0, slope=None):
        self.type = vtype
        self.fuel_type = fuel_type
        self.segment = segment
        self.euro_std = euro_std
        self.mode = mode
        self.load = load
        self.height = height
        self.length = length
        self.slope = slope

    @staticmethod
    def get_type_for_category(category_id):
        return Vehicle.mapping.get(category_id, None)

    def get_category_id(self):
        for cat_id, name in six.iteritems(self.mapping):
            if name == self.type:
                return cat_id


class LCategory(Vehicle):
    """Scooters, 2 and 3-wheels
    """
    def __init__(self, fuel_type=FuelTypes.PETROL, subsegment='', euro_std='', mode='', load=-1.0, height=1.5, length=2.5):
        super(LCategory, self).__init__(VehicleTypes.LCATEGORY, fuel_type, subsegment, euro_std, mode, load, height, length)


class Car(Vehicle):
    """Regular passenger car
        subsegment_id: Mini
        subsegment_id: Small
        subsegment_id: Medium
        subsegment_id: Large-SUV-Executive
    """

    def __init__(self, fuel_type=FuelTypes.PETROL, subsegment='Small', euro_std='Euro 4', mode=''):
        super(Car, self).__init__(VehicleTypes.CAR, fuel_type, subsegment, euro_std, mode)


class Van(Vehicle):
    """Light Commercial Car
        subsegment_id: N1-I
        subsegment_id: N1-II
        subsegment_id: N1-III
    """
    def __init__(self, fuel_type=FuelTypes.DIESEL, subsegment='N1-I', euro_std='Euro 4', mode=''):
        super(Van, self).__init__(VehicleTypes.VAN, fuel_type, subsegment, euro_std, mode)


class Bus(Vehicle):
    """Buses
    subsegment_id: Urban Buses Midi <=15 t
    subsegment_id: Urban Buses Standard 15 - 18 t
    subsegment_id: Urban Buses Articulated >18 t
    subsegment_id: Coaches Standard <=18 t
    subsegment_id: Coaches Articulated >18 t
    """
    def __init__(self, fuel_type=FuelTypes.DIESEL, subsegment='Conventional', euro_std='Euro I', mode='', load=0.0):
        super(Bus, self).__init__(VehicleTypes.BUS, fuel_type, subsegment, euro_std, mode, load)


class Truck(Vehicle):
    """Heavy Duty Trucks
    subsegment_id: Articulated 14 - 20 t
    subsegment_id: Articulated 20 - 28 t
    subsegment_id: Articulated 28 - 34 t
    subsegment_id: Articulated 34 - 40 t
    subsegment_id: Articulated 40 - 50 t
    subsegment_id: Articulated 50 - 60 t
    subsegment_id: Rigid 12 - 14 t
    subsegment_id: Rigid 14 - 20 t
    subsegment_id: Rigid 20 - 26 t
    subsegment_id: Rigid 26 - 28 t
    subsegment_id: Rigid 28 - 32 t
    subsegment_id: Rigid >32 t
    subsegment_id: Rigid 7.5 - 12 t
    subsegment_id: Rigid <=7.5 t
    """
    def __init__(self, fuel_type=FuelTypes.DIESEL, subsegment='Articulated 14 - 20 t', euro_std='Euro I', mode='', load=0.0, slope=0.0):
        super(Truck, self).__init__(VehicleTypes.TRUCK, fuel_type, subsegment, euro_std, mode=mode, load=load, slope=slope)
