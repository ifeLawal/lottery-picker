import datetime
from datetime import date, timedelta

from bizlogic.database_operations import (get_tickets_played,
                                          get_winning_numbers,
                                          save_tickets_to_db, update_winnings,
                                          update_winnings_of_our_tickets)
from bizlogic.number_pickers import (create_tickets, get_ordered_megaball,
                                     get_random_regular_numbers)
from bizlogic.scrape_mega_millions import \
    scrape_most_recent_mega_millions_number


# Run this on Wed / Sat
def pull_latest_mega_millions_winning_ticket() -> None:
    scrape_most_recent_mega_millions_number(1)


# Run this on Tue / Fri
def create_tickets_and_save(
    number_of_tickets: int, ticket_type: str = "random"
) -> None:
    array_of_tickets = create_tickets(
        number_of_tickets=number_of_tickets,
        get_regular_numbers=get_random_regular_numbers,
        generate_megaball=get_ordered_megaball,
    )

    draw_date = datetime.datetime.strptime(date.today(), "%m/%d/%Y/")

    save_tickets_to_db(
        ticket_type=ticket_type, tickets=array_of_tickets, date=draw_date
    )


# Run this on Wed / Sat after pulling the latest winner
def update_guess_tickets_by_type(ticket_type: str = "random") -> None:
    date_time_obj = datetime.datetime.strptime(
        date.today(), "%m/%d/%Y/"
    ) - timedelta(days=1)
    draw_date = date_time_obj.strftime("%m/%d/%Y/")
    
    update_winnings(ticket_type=ticket_type, draw_date=draw_date)
    get_tickets_played(draw_date=draw_date, order_by="winnings")
