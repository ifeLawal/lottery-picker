from datetime import date
import datetime

from bizlogic.database_operations import (get_tickets_played,
                                          save_tickets_to_db, update_winnings)
from bizlogic.number_pickers import (create_tickets, get_ordered_megaball,
                                     get_random_regular_numbers)
from bizlogic.scrape_mega_millions import \
    scrape_most_recent_mega_millions_number


# Run this on Wed / Sat
def pull_latest_mega_millions_winning_ticket() -> None:
    scrape_most_recent_mega_millions_number(1)


# Run this on Tue / Fri
def create_tickets_and_save(number_of_tickets: int, ticket_type: str = "random") -> str:
    array_of_tickets = create_tickets(
        number_of_tickets=number_of_tickets,
        get_regular_numbers=get_random_regular_numbers,
        generate_megaball=get_ordered_megaball,
    )

    draw_date = date.today()
    
    save_tickets_to_db(
        ticket_type=ticket_type, tickets=array_of_tickets, date=draw_date
    )
    tickets_in_string = "<h1>Tickets created</h1>"
    counter = 1
    for ticket in array_of_tickets:
        temp_string = ", ".join(str(n).zfill(2) for n in ticket)
        tickets_in_string += f"{str(counter).zfill(2)}. {temp_string}<br />"
        counter += 1
    return tickets_in_string


# Run this on Wed / Sat after pulling the latest winner
def update_guess_tickets_by_type(ticket_type: str = "random") -> str:
    # yesterday = date.today() - timedelta(days = 1)
    draw_date = date.today()  # yesterday.strptime("%m/%d/%Y/").date()

    (winner, config_row) = update_winnings(ticket_type=ticket_type)
    array_of_tickets = get_tickets_played(draw_date=draw_date, order_by="winnings")
    tickets_in_string = f"""
        <h1>Ticket Winning Status</h1> 
        <p>{config_row.keys()} </p> 
        <h3>Overall metrics: {config_row}</h3> 
        <h3>Winning ticket: {winner} </h3>
        <p>{array_of_tickets[0].keys()}</p>
    """
    counter = 1
    for ticket in array_of_tickets:
        tickets_in_string += f"{str(counter).zfill(2)}. {ticket.__repr__()} <br />"
        counter += 1
    return tickets_in_string
