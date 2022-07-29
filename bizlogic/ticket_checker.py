from datetime import date
from bizlogic.mega_millions import Session
from bizlogic.number_pickers import create_tickets, random_ticket_creation, ordered_megaball
from datastore.models.mega_millions import Winners

def check_tickets(ticket: list, date: date) -> str:
    draw_date = "07/26/22"
    with Session() as session:
        winner = session.query(Winners).filter(Winners.draw_date == draw_date)
        winning_ticket = {str(winner.first_number):""} [, winner.second_number, winner.third_number, winner.fourth_number, winner.fifth_number, winner.mega_ball]
    
    # pull the latest winning numbers
    # check if your tickets won
    pass