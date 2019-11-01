import sys

from country import Country
from utils import FileReader, FormatError
from world import World


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

        thread = world.run()
        if thread:
            threads.append(thread)
            thread.start()
        else:
            Country.clean_cash(len(threads) + 1)

    for thread in threads:
        thread.join()

    res = sorted(World.result)

    for key in res:
        print("Case Number ", key)
        for country in sorted(World.result[key]):
            print(country[1], country[0])


if __name__ == "__main__":
    main(sys.argv)
