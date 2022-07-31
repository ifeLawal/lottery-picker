from datetime import date
from bizlogic import constants
from bizlogic.mega_millions import Session
from bizlogic.number_pickers import create_tickets, random_ticket_creation, ordered_megaball
from datastore.models.mega_millions import Winners

def check_tickets(ticket: list, date: date):
    draw_date = "07/26/22"
    with Session() as session:
        winner = session.query(Winners).filter(Winners.draw_date == draw_date)
        # winning_ticket = {str(winner.first_number):""} [, winner.second_number, winner.third_number, winner.fourth_number, winner.fifth_number, winner.mega_ball]
        # 
        
    return [{"23": constants.MATCHED, "43": constants.UNMATCHED}]

def check_ticket(ticket: list, winners: object) -> object:
    ticket_results = {}
    for num in ticket:
        if winners[num]:
            ticket_results[num] = constants.MATCHED
        else:
            ticket_results[num] = constants.UNMATCHED
    return ticket_results

def check_winnings_for_a_ticket(ticket: object) -> int:
    
    return 0