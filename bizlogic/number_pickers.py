import random
from bizlogic.mega_millions import Session
from bizlogic import constants
from datastore.models.mega_millions_generated_data import PureRandomTicketAttempts
from datetime import date

regular_numbers_needed = 5

def create_wednesday_tickets():
    date.today()
    

# pick at random from the 
def random_megaball(number_of_tickets: int) -> list:
    arr_megaball = []
    for _ in range(number_of_tickets):
        arr_megaball.append(pick_mega_ball())
    return arr_megaball

# 
def random_ticket_creation(number_of_tickets: int) -> list:
    arr_of_tickets = []
    for _ in range(number_of_tickets):
        arr_of_tickets.append(pick_numbers())
    return arr_of_tickets

# 
def megaball_weighted(number_of_tickets: int) -> list:
    arr_megaball = []
    if number_of_tickets > constants.MEGA_BALL_MAX:
        for _ in range(constants.MEGA_BALL_MAX):
            arr_megaball.append(i)
    return arr_megaball

# 
def ordered_megaball(number_of_tickets: int) -> list:
    arr_megaball = []
    counter = 1
    for _ in range(number_of_tickets):
        arr_megaball.append(counter)
        counter += 1
        if counter > constants.MEGA_BALL_MAX:
            counter = 1
    return arr_megaball

def create_tickets(date: date, number_of_tickets: int, generate_tickets, generate_megaball) -> list:
    arr_ticket = generate_tickets(number_of_tickets)
    arr_megaball = generate_megaball(number_of_tickets)
    for i in range(number_of_tickets):
        arr_ticket[i].append(arr_megaball[i])
    return arr_ticket
        

def save_tickets_to_db(ticket_type: str, tickets: list):
    for arr in tickets:
        with Session() as session:
                new_ticket = PureRandomTicketAttempts(
                    draw_date=date.today(),
                    first_number=arr[0],
                    second_number=arr[1],
                    third_number = arr[2],
                    fourth_number = arr[3],
                    fifth_number = arr[4],
                    mega_ball = arr[5]
                )
                session.add(new_ticket)
                session.commit()
    pass

def pick_numbers() -> list:
    return random.sample(range(constants.REGULAR_NUMBER_START, constants.REGULAR_NUMBER_MAX), constants.MEGA_BALL_NUMBERS_NEEDED)
    
def pick_mega_ball() -> int:
    return random.randint(constants.MEGA_BALL_START, constants.MEGA_BALL_MAX)