from copy import copy

from utils import Point


class City(object):
    _city_cash = {}

    def __init__(self, point, country, world_id=1):
        self.__point = point
        self._coins = {country: 1000000}
        self._daily_income = {}
        self.__world_id = world_id
        if self._city_cash.get(world_id):
            self._city_cash[world_id].update({point.get_coord(): self})
        else:
            self._city_cash[world_id] = {point.get_coord(): self}

    def get_coords(self):
        return self.__point.x, self.__point.y

    def __get_neighbor(self):
        neighbors = []

        neighbors.append(self._city_cash[self.__world_id].get((self.__point.x, self.__point.y + 1), None))  # north neighbor
        neighbors.append(self._city_cash[self.__world_id].get((self.__point.x + 1, self.__point.y), None))  # east neighbor
        neighbors.append(self._city_cash[self.__world_id].get((self.__point.x, self.__point.y - 1), None))  # south neighbor
        neighbors.append(self._city_cash[self.__world_id].get((self.__point.x - 1, self.__point.y), None))  # west neighbor

        return neighbors

    def add_coins(self, income):
        for coin_motif, coin_count in income.items():
            self._daily_income[coin_motif] = self._daily_income.get(coin_motif, 0) + coin_count

    def __representative_portion_count(self):
        return {coin_motif: coin_count // 1000 for coin_motif, coin_count in self._coins.items() if coin_count // 1000}

    def share_coins(self):
        repr_portion = self.__representative_portion_count()
        for neighbor in self.__get_neighbor():
            if neighbor:
                for coin_motif, coin_count in repr_portion.items():
                    self._coins[coin_motif] = self._coins.get(coin_motif, 0) - coin_count
                neighbor.add_coins(repr_portion)

    def update_balance(self):
        for coin_motif, coin_count in self._daily_income.items():
            self._coins[coin_motif] = self._coins.get(coin_motif, 0) + coin_count
        self._daily_income = {}

    @property
    def motif_count(self):
        return len(self._coins)
