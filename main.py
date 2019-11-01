import sys
from threading import Thread

from world import World
from country import Country
from utils import FileReader, FormatError


def main(argv):
    if len(argv) != 2:
        return 1

    input_file = argv[1]

    file_reader = FileReader(input_file)
    threads = []

    while True:
        try:
            raw_world = file_reader.get_world()
        except StopIteration:
            break
        except FormatError:
            continue

        world = World(len(threads) + 1, raw_world)
        if world.is_init:
            if world.check_connections():
                threads.append(Thread(target=world.world_handler))
                threads[-1].start()
            else:
                print("Sorry but not all country connect. World: {}".format(world.countries_names))
                Country.clean_cash(len(threads) + 1)
                continue

    for thread in threads:
        thread.join()

    res = sorted(World.result)

    for key in res:
        print("Case Number ", key)
        for country in sorted(World.result[key]):
            print(country[1], country[0])


if __name__ == "__main__":
    main(sys.argv)
