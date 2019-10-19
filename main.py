import sys
import time
from threading import Thread

from country import Country
from utils import FileReader, Point

result = {}


def parse(file_reader):
    universe = []

    while True:
        world = []
        raw_world = file_reader.get_world()

        if not raw_world:
            break

        for raw_country in raw_world:
            country_name, coords = raw_country
            xl, yl, xh, yh = coords.split()

            bottom_point = Point(int(xl), int(yl))
            top_point = Point(int(xh), int(yh))

            world.append(Country(bottom_point, top_point, country_name, len(universe)))

        if world:
            universe.append(world)

    return universe


def world_handler(world, case_num):
    while not all([country.is_complete for country in world]):
        for country in world:
            country.start_day()

        for country in world:
            country.end_day()

    res = [(country.complete_day, country.name) for country in world]

    result[case_num] = res


def main(argv):
    if len(argv) != 2:
        return 1

    input_file = argv[1]

    file_reader = FileReader(input_file)
    universe = parse(file_reader)

    threads = []

    for world in universe:
        threads.append(Thread(target=world_handler, args=(world, universe.index(world))))
        threads[-1].start()

    for thread in threads:
        thread.join()

    res = sorted(result)

    for key in res:
        print("Case Number ", key)
        for country in sorted(result[key]):
            print(country[1], country[0])


if __name__ == "__main__":
    start = time.process_time()
    main(sys.argv)
    print(time.process_time()-start)