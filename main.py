# https://www.lottoamerica.com/mega-millions/statistics
import sys

from multipledispatch import dispatch

from bizlogic.generate_stats import (get_percent_for_all_numbers,
                                     set_connected_number_occurrences)
from bizlogic.notifier import email_lottery_run_msg
from bizlogic.orchestrator import (create_tickets_and_save,
                                   pull_latest_mega_millions_winning_ticket,
                                   update_guess_tickets_by_type)
from bizlogic.scrape_mega_millions import (
    scrape_all_mega_millions_numbers, scrape_most_recent_mega_millions_number)


def experiment() -> None:
    print({str(1): 1})
    get_percent_for_all_numbers()
    set_connected_number_occurrences()


@dispatch()
def run() -> None:
    scrape_all_mega_millions_numbers()


@dispatch(list)
def run(args: list) -> None:
    if args[0] == "renew":
        print("renew running")
        scrape_all_mega_millions_numbers()
        message = "we ran the renew script"
    elif args[0] == "latest":
        print("latest running")
        scrape_most_recent_mega_millions_number(1)
        message = "we ran the latest script"
    elif args[0] == "check_winnings":
        pull_latest_mega_millions_winning_ticket()
        message = update_guess_tickets_by_type(args[1])
    elif args[0] == "create_tickets":
        message = create_tickets_and_save(int(args[1]))
    email_lottery_run_msg(message)


if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    function = globals()[args[1]]
    print(args[2:])
    function(args[2:])
    # scrape_most_recent_mega_millions_number()
