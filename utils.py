import dataclasses
from copy import copy


@dataclasses.dataclass()
class Point(object):
    x: int
    y: int

    def get_coord(self):
        return self.x, self.y

    def __le__(self, other):
        return self.y < other.y or (self.y == other.y and self.x <= other.x)

    class __IterablePoint(object):
        def __init__(self, start_pos, stop_pos):
            self.__start_pos = start_pos
            self.__stop_pos = stop_pos
            self.__current_pos = None

        def __iter__(self):
            self.__current_pos = copy(self.__start_pos)
            return self

        def __next__(self):
            if self.__current_pos <= self.__stop_pos:
                res = Point(*self.__current_pos.get_coord())
                if self.__current_pos.x == self.__stop_pos.x:
                    self.__current_pos.x = self.__start_pos.x
                    self.__current_pos.y += 1
                else:
                    self.__current_pos.x += 1
                return res
            else:
                raise StopIteration

    @staticmethod
    def iterate(from_point, to_point):
        return Point.__IterablePoint(from_point, to_point)


class FormatError(Exception):
    pass


class FileReader(object):
    def __init__(self, input_file="input.txt"):
        self._input_file = open(input_file)
        self.is_close = False

    def __get_line(self):
        if not self._input_file.closed:
            for line in self._input_file:
                yield line
            self._input_file.close()
            return None

    def get_world(self):
        reader = self.__get_line()
        counties_count = 0
        while True:
            data = next(reader)

            try:
                counties_count = int(data)
            except ValueError:
                print("count must be integer: {}".format(data))
                raise FormatError

            world = []

            for i in range(counties_count):
                world.append(next(reader))

            return world
