import re
from threading import Thread

from country import Country
from utils import Point


class World(object):
    result = {}

    def __init__(self, world_id, raw_world):
        self.__world_id = world_id
        self._countries = []

        self.is_init = False

        self.__parse(raw_world)

    def __parse(self, raw_world):
        reg_pattern = r'\b[A-Za-z]{1,25}\b(\s\d){4}'

        regex = re.compile(reg_pattern)

        if not raw_world:
            return None

        for raw_country in raw_world:
            if regex.match(raw_country):
                country_name, coords = raw_country.split(maxsplit=1)
                try:
                    xl, yl, xh, yh = coords.split()
                except ValueError:
                    print("Must be four cordinates: {}".format(coords))
                    Country.clean_cash(self.__world_id)
                    return

                xl, yl, xh, yh = int(xl), int(yl), int(xh), int(yh)

                if xl > xh or yl > yh:
                    print("Second coord must be bigger or equal that first: {}".format(coords))
                    Country.clean_cash(self.__world_id)
                    return

                if xl <= 0 or xh <= 0 or yl <= 0 or yh <= 0:
                    print("Coords have to be positive".format(coords))
                    Country.clean_cash(self.__world_id)
                    return

                bottom_point = Point(xl, yl)
                top_point = Point(xh, yh)

                self._countries.append(Country(bottom_point, top_point, country_name, self.__world_id))
            else:
                print("Country format error: {}".format(raw_country))
                Country.clean_cash(self.__world_id)
                return

        self.is_init = True

    def world_handler(self):
        while not all([country.is_complete for country in self._countries]):
            for country in self._countries:
                country.start_day()

            for country in self._countries:
                country.end_day()

        res = [(country.complete_day, country.name) for country in self._countries]

        World.result[self.__world_id] = res

    def check_connections(self):
        return len(self._countries) == len(self.__path_builder())

    def __path_builder(self, country=None, neighbors=None):

        if not country:
            country = self._countries[0]

        if neighbors is None:
            neighbors = {country}
        else:
            neighbors.add(country)

        new_neighbors = country.neighbours.difference(neighbors)

        for count in new_neighbors:
            neighbors.update(self.__path_builder(count, neighbors))

        return neighbors

    def run(self):
        if self.is_init:
            if self.check_connections():
                return Thread(target=self.world_handler)
            else:
                print("Not all country can be connect. World: {}".format(self.countries_names()))
                Country.clean_cash(self.__world_id)
                return None

    def countries_names(self):
        return [country.name for country in self._countries]
