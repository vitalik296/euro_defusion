class City(object):
    __BASE_COINS_COUNT = 1000000
    __COIN_PORTION = 1000

    _city_cash = {}

    def __init__(self, point, country, world_id=1):
        self.country = country
        self.__point = point
        self._coins = {country.name: self.__BASE_COINS_COUNT}
        self._daily_income = {}
        self.__world_id = int(world_id)

        self.__neighbors = set()

        if self._city_cash.get(self.__world_id):
            self._city_cash[self.__world_id].update({point.get_coord(): self})
        else:
            self._city_cash[self.__world_id] = {point.get_coord(): self}

    def get_coords(self):
        return self.__point.x, self.__point.y

    def get_neighbors(self):
        north_neighbor = self._city_cash[self.__world_id].get((self.__point.x, self.__point.y + 1), None)
        if north_neighbor:
            self.add_neighbor(north_neighbor)
            north_neighbor.add_neighbor(self)

        east_neighbor = self._city_cash[self.__world_id].get((self.__point.x + 1, self.__point.y), None)
        if east_neighbor:
            self.add_neighbor(east_neighbor)
            east_neighbor.add_neighbor(self)

        south_neighbor = self._city_cash[self.__world_id].get((self.__point.x, self.__point.y - 1), None)
        if south_neighbor:
            self.add_neighbor(south_neighbor)
            south_neighbor.add_neighbor(self)

        west_neighbor = self._city_cash[self.__world_id].get((self.__point.x - 1, self.__point.y), None)
        if west_neighbor:
            self.add_neighbor(west_neighbor)
            west_neighbor.add_neighbor(self)

    def add_coins(self, income):
        for coin_motif, coin_count in income.items():
            self._daily_income[coin_motif] = self._daily_income.get(coin_motif, 0) + coin_count

    def __representative_portion_count(self):
        return {coin_motif: coin_count // self.__COIN_PORTION for coin_motif, coin_count in self._coins.items() if
                coin_count // self.__COIN_PORTION}

    def share_coins(self):
        repr_portion = self.__representative_portion_count()

        for neighbor in self.__neighbors:
            if neighbor:
                for coin_motif, coin_count in repr_portion.items():
                    self._coins[coin_motif] = self._coins.get(coin_motif, 0) - coin_count
                neighbor.add_coins(repr_portion)

    def update_balance(self):
        for coin_motif, coin_count in self._daily_income.items():
            self._coins[coin_motif] = self._coins.get(coin_motif, 0) + coin_count
        self._daily_income = {}

    def add_neighbor(self, city):
        self.__neighbors.add(city)
        self.country.neighbours.add(city.country)

    @property
    def motif_count(self):
        return len(self._coins)

    @staticmethod
    def clean_cash(world_id):
        del City._city_cash[int(world_id)]