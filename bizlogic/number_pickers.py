import random
from bizlogic.mega_millions import dao
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
    arr = []
    for i in range(70):
        arr.append(i)
    counter = 0
    for _ in range(number_of_tickets):
        numbers = []
        random.shuffle(arr)
        for i in range(5):
            numbers.append(arr[counter])
            counter += 1
            if counter >= len(arr):
                counter = 0
                random.shuffle(arr)

        arr_of_tickets.append(numbers)

    # for _ in range(number_of_tickets):
    #     arr_of_tickets.append(pick_numbers())
    return arr_of_tickets


#
def megaball_weighted(number_of_tickets: int) -> list:
    arr_megaball = []
    if number_of_tickets > constants.MEGA_BALL_MAX:
        for _ in range(constants.MEGA_BALL_MAX):
            arr_megaball.append(i)  # TODO figure out what i is aka the weighted number
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


def create_tickets(
    number_of_tickets: int, generate_tickets, generate_megaball, date: date
) -> list:
    arr_ticket = generate_tickets(number_of_tickets)
    arr_megaball = generate_megaball(number_of_tickets)
    for i in range(number_of_tickets):
        arr_ticket[i].append(arr_megaball[i])
    return arr_ticket


def save_tickets_to_db(ticket_type: str, tickets: list):
    ins = dao.pure_random_ticket_attempts.insert()
    if ticket_type == "random":
        ins = dao.pure_random_ticket_attempts.insert()
    for arr in tickets:
        dao.connection.execute(
            ins,
            draw_date=date.today(),
            first_number=arr[0],
            second_number=arr[1],
            third_number=arr[2],
            fourth_number=arr[3],
            fifth_number=arr[4],
            mega_ball=arr[5],
        )
    pass


def pick_numbers() -> list:
    return random.sample(
        range(constants.REGULAR_NUMBER_START, constants.REGULAR_NUMBER_MAX),
        constants.MEGA_BALL_NUMBERS_NEEDED,
    )


def pick_mega_ball() -> int:
    return random.randint(constants.MEGA_BALL_START, constants.MEGA_BALL_MAX)
