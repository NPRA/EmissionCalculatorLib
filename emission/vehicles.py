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
    def __init__(self, vtype, fuel_type, segment, euro_std, mode='', load=-1.0):
        self.type = vtype
        self.fuel_type = fuel_type
        self.segment = segment
        self.euro_std = euro_std
        self.mode = mode
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
    def __init__(self, fuel_type, subsegment='', euro_std='', mode=''):
        super(LCategory, self).__init__(VehicleTypes.LCATEGORY, fuel_type, subsegment, euro_std)


class Car(Vehicle):
    """Regular passenger car
        subsegment_id: Mini
        subsegment_id: Small
        subsegment_id: Medium
        subsegment_id: Large-SUV-Executive
    """
    # type = [{
    #     'Mini': [{
    #         "Petrol": ['Euro 4', 'Euro 5','Euro 6', 'Euro 6 up to 2016', 'Euro 6 2017-2019', 'Euro 6 2020+']
    #     }]
    #     },
    #     {
    #     'Small': ['Conventional',
    #               'PRE ECE',
    #               'ECE 15/00-01',
    #               'ECE 15/02',
    #               'ECE 15/03',
    #               'ECE 15/04',
    #               'Improved Conventional',
    #               'Open Loop',
    #               'Euro 1', 'Euro 2', 'Euro 3', 'Euro 4', 'Euro 5',
    #               'Euro 6 up to 2016', 'Euro 6 2017-2019', 'Euro 6 2020+']
    #     },
    #     {
    #     'Medium': ['PRE ECE',
    #                'ECE 15/00-01',
    #                'ECE 15/02',
    #                'ECE 15/03',
    #                'ECE 15/04',
    #                'Improved Conventional',
    #                'Open Loop',
    #                'Euro 1', 'Euro 2', 'Euro 3', 'Euro 4', 'Euro 5',
    #                'Euro 6 up to 2016', 'Euro 6 2017-2019', 'Euro 6 2020+']
    #     },
    #     {
    #     'Large-SUV-Executive':['Conventional',
    #                            'PRE ECE',
    #                            'ECE 15/00-01',
    #                            'ECE 15/02',
    #                            'ECE 15/03',
    #                            'ECE 15/04',
    #                            'Euro 1', 'Euro 2', 'Euro 3', 'Euro 4', 'Euro 5',
    #                            'Euro 6 up to 2016', 'Euro 6 2017-2019', 'Euro 6 2020+']
    #     }
    # ]

    def __init__(self, fuel_type, subsegment='Small', euro_std='Euro 4', mode=''):
        super(Car, self).__init__(VehicleTypes.CAR, fuel_type, subsegment, euro_std)


class Van(Vehicle):
    """Light Commercial Car
        subsegment_id: N1-I
        subsegment_id: N1-II
        subsegment_id: N1-III
    """
    def __init__(self, fuel_type, subsegment='N1-I', euro_std='Euro 4', mode=''):
        super(Van, self).__init__(VehicleTypes.VAN, fuel_type, subsegment, euro_std)


class Bus(Vehicle):
    """Buses
    subsegment_id: Urban Buses Midi <=15 t
    subsegment_id: Urban Buses Standard 15 - 18 t
    subsegment_id: Urban Buses Articulated >18 t
    subsegment_id: Coaches Standard <=18 t
    subsegment_id: Coaches Articulated >18 t
    """
    def __init__(self, fuel_type, subsegment='Conventional', euro_std='Euro I', mode='', load=0.0):
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
    def __init__(self, fuel_type, subsegment='Articulated 14 - 20 t', euro_std='Euro I', mode='', load=0.0):
        super(Truck, self).__init__(VehicleTypes.TRUCK, fuel_type, subsegment, euro_std, mode, load)
