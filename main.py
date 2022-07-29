import random
import sys
from multipledispatch import dispatch

from bizlogic.mega_millions import (scrape_all_mega_millions_numbers,
                                   scrape_most_recent_mega_millions_number)

def experiment() -> None:
    print({str(1): 1})
    # print(random_array)
    # print(set([frozenset([1, 2]), frozenset([2, 3])]))
    # print(set([frozenset([1, 2]), frozenset([2, 3])]).__len__())
    # print(set([frozenset([1, 2]), frozenset([2, 1])]))
    # print(set([frozenset([1, 2]), frozenset([2, 1])]).__len__())

@dispatch()
def run() -> None:
    scrape_all_mega_millions_numbers()

@dispatch(str)
def run(type: str) -> None:   
    if type == "renew":
        scrape_all_mega_millions_numbers()
    elif type == "latest":
        scrape_most_recent_mega_millions_number()

if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    function = globals()[args[1]]
    function(*args[2:])
    # scrape_most_recent_mega_millions_number()