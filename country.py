from city import City
from utils import Point


class Country(object):
    _country_cash = {}

    def __init__(self, left_bottom_point, right_top_point, name, world_id=1):
        self.name = name
        self.is_complete = False
        self.__cities = []
        self.complete_day = 0
        self.__world_id = int(world_id)

        self.neighbours = {self}

        self.__generate_cities(left_bottom_point, right_top_point)

        if self._country_cash.get(self.__world_id):
            self._country_cash[self.__world_id].append(self)
        else:
            self._country_cash[self.__world_id] = [self]

    def __generate_cities(self, left_bottom_point, right_top_point):
        for point in Point.iterate(left_bottom_point, right_top_point):
            self.__cities.append(City(point, self, self.__world_id))
            self.__cities[-1].get_neighbors()

    def start_day(self):
        if all([city.motif_count == len(self._country_cash[self.__world_id]) for city in self.__cities]):
            self.is_complete = True

        if not self.is_complete:
            self.complete_day += 1

        for city in self.__cities:
            city.share_coins()

    def end_day(self):
        for city in self.__cities:
            city.update_balance()

    @staticmethod
    def clean_cash(world_id):
        world_id = int(world_id)
        if world_id in Country._country_cash:
            del Country._country_cash[int(world_id)]
            City.clean_cash(int(world_id))

    def clear(self):
        Country.clean_cash(self.__world_id)
