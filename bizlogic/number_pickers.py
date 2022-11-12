import random
from datetime import date

from bizlogic import constants


# =============== Regular Number Strategies Start ================

#
def get_random_regular_numbers(number_of_tickets: int) -> list:
    arr_of_tickets = []
    regular_numbers_array = []
    for i in range(70):
        regular_numbers_array.append(i)
    counter = 0
    for _ in range(number_of_tickets):
        numbers = []
        random.shuffle(regular_numbers_array)
        for i in range(5):
            numbers.append(regular_numbers_array[counter])
            counter += 1
            if counter >= len(regular_numbers_array):
                counter = 0
                random.shuffle(regular_numbers_array)

        arr_of_tickets.append(numbers)

    # for _ in range(number_of_tickets):
    #     arr_of_tickets.append(pick_numbers())
    return arr_of_tickets


def get_regular_numbers() -> list:
    return random.sample(
        range(constants.REGULAR_NUMBER_START, constants.REGULAR_NUMBER_MAX),
        constants.AMT_OF_REGULAR_NUMBERS_NEEDED,
    )


# =============== Regular Number Strategies End ================

# =============== Mega Ball Strategies Start ================

# pick at random from the
def get_random_megaball(number_of_tickets: int) -> list:
    arr_megaball = []
    for _ in range(number_of_tickets):
        arr_megaball.append(get_megaball())
    return arr_megaball


#
def get_weighted_megaball(number_of_tickets: int) -> list:
    arr_megaball = []
    if number_of_tickets > constants.MEGA_BALL_MAX:
        for _ in range(constants.MEGA_BALL_MAX):
            # TODO figure out what i is aka the weighted number
            arr_megaball.append(i)
    return arr_megaball


#
def get_ordered_megaball(number_of_tickets: int) -> list:
    arr_megaball = []
    counter = 1
    for _ in range(number_of_tickets):
        arr_megaball.append(counter)
        counter += 1
        if counter > constants.MEGA_BALL_MAX:
            counter = 1
    return arr_megaball


def get_megaball() -> int:
    return random.randint(constants.MEGA_BALL_START, constants.MEGA_BALL_MAX)


# =============== Mega Ball Strategies End ================

# =============== Full Ticket Strategies Start ================


# create_tickets is a generic method for creating tickets
# you pass in the strategy for getting the regular numbers
# and getting the megaball
# and it compiles to two to give you a complete ticket
# this makes it flexible to merge strategies ie pure random, weighted, and more
def create_tickets(
    number_of_tickets: int, get_regular_numbers, generate_megaball
) -> list:
    arr_ticket = get_regular_numbers(number_of_tickets)
    arr_megaball = generate_megaball(number_of_tickets)
    for i in range(number_of_tickets):
        arr_ticket[i].append(arr_megaball[i])
    return arr_ticket


# =============== Full Ticket Strategies End ================
