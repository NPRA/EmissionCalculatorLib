def enum(**named_values):
    return type('Enum', (), named_values)


types = enum(FC='FC', PM='PM', HC='HC', CO='CO', NOx='NOx')


class Pollutants:
    def __init__(self, paths):
        self._pollutants = {}
        self._paths = paths

    def add_pollutant(self, name, is_visible):
        if is_visible:
            self._pollutants[name] = [[] for x in range(self._paths)]

    def __getitem__(self, item):
        return self._pollutants[item]

    def __iter__(self):
        return iter(sorted(self._pollutants))

    def __call__(self):
        return sorted(self._pollutants)

    def __len__(self):
        return len(self._pollutants)
