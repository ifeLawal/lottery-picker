from datetime import date

from bizlogic import constants
from datastore.models.mega_millions import dao

winning_options = {
    "5win": 1000000,
    "5winmega": 1000000,
    "4win": 500,
    "4winmega": 10000,
    "3win": 10,
    "3winmega": 200,
    "2win": 0,
    "2winmega": 10,
    "1win": 0,
    "1winmega": 4,
    "mega": 2,
}

# TODO convert this into a get_matches method that works for a single and multiple tickets
def get_matches_for_tickets(tickets: list, date: date) -> tuple:
    """ """
    regular_ticket_matches = []
    mega_ball_ticket_matches = []
    draw_date = "07/26/2022"
    with dao.session() as session:
        # winning regular numbers
        # {"64": True, "12": True, "33": True, "19": True, "23": True}
        # winning mega ball number
        # {"12": True}
        winner = session.query(dao.winners).filter(dao.winners.c.draw_date == draw_date)
        regular_number_wins = {
            str(winner.first_number): True,
            str(winner.second_number): True,
            str(winner.third_number): True,
            str(winner.fourth_number): True,
            str(winner.fifth_number): True,
        }
        mega_ball_winner = {str(winner.mega_ball): True}

    for ticket in tickets:
        # regular matches structure:
        #  R1,                R2,               R3,            R4,            R5
        # {"50": "no match", "15": "no match", "64": "match", "19": "match", "23": "match"}
        # mega ball matches structure:
        # {"12": "match"}
        regular_matches, mega_ball_matches = get_number_matches_on_ticket(
            ticket=ticket,
            regular_winners=regular_number_wins,
            mega_ball_winner=mega_ball_winner,
        )
        regular_ticket_matches.append(regular_matches)
        mega_ball_ticket_matches.append(mega_ball_matches)

    return regular_ticket_matches, mega_ball_ticket_matches


def get_number_matches_on_ticket(
    ticket: list, regular_winners: object, mega_ball_winner: object
) -> object:
    """
    :return: regular number matches and mega ball matches
    :rtype: tuple sample - ({"64": True, "12": True, "33": True, "19": True, "23": True}, {"12": True})
    """
    regular_number_results = {}
    mega_ball_number_results = {}
    counter = 0
    # single ticket structure:
    # R - regular ball
    # M - mega ball
    #  R1, R2, R3, R4, R5, M1
    # [12, 32, 41, 23, 14, 12]
    for num in ticket:
        counter += 1
        str_num = str(num)
        if counter <= 5:
            if str_num in regular_winners.keys():
                regular_number_results[str_num] = constants.MATCHED
            else:
                regular_number_results[str_num] = constants.UNMATCHED
        else:
            if str_num in mega_ball_winner.keys():
                mega_ball_number_results[str_num] = constants.MATCHED
            else:
                mega_ball_number_results[str_num] = constants.UNMATCHED
    return regular_number_results, mega_ball_number_results
    # regular number results structure:
    #  R1,                R2,               R3,            R4,            R5
    # {"50": "no match", "15": "no match", "64": "match", "19": "match", "23": "match"}
    # mega ball matches structure:
    # {"12": "match"}


# TODO convert this into a check_winnings method that works for a single and multiple tickets
def check_winnings_for_multiple_tickets(tickets: list, date: str) -> int:
    """ """
    # draw_date = "07/26/2022"  # TODO use the date parameter rather than hardcoded
    with dao.session() as session:
        winner = (
            session.query(dao.winners).filter(dao.winners.c.draw_date == date).first()
        )
        regular_number_wins = {
            str(winner.first_number): True,
            str(winner.second_number): True,
            str(winner.third_number): True,
            str(winner.fourth_number): True,
            str(winner.fifth_number): True,
        }
        mega_ball_winner = {str(winner.mega_ball): True}

    # ticket structure:
    # R - regular number wins
    # M - mega ball winner
    #  R1,         R2,         R3,         R4,          R5
    # {"64": True, "12": True, "33": True, "19": True, "23": True}
    #  M1
    # {"12": True}
    total_wins = 0
    for ticket in tickets:
        total_wins += check_winnings_for_a_ticket(
            ticket=ticket,
            regular_winners=regular_number_wins,
            mega_ball_winner=mega_ball_winner,
        )
    return total_wins


def check_winnings_for_a_ticket(
    ticket: list, regular_winners: object, mega_ball_winner: object
) -> int:
    """
    check how much is won from the ticket numbers

    :param object ticket: a tickets list of numbers. sample - [64, 12, 33, 19, 23, 12]
    :param object regular_winners: winning ticket numbers. sample - {"64": True, "12": True, "33": True, "19": True, "23": True}
    :param object mega_ball_winner: winning mega ball number. sample - {"12": True}
    :return: the winnings
    :rtype: int sample - 10
    """
    # If a player matches all five numbers, but not the “Mega Ball,” then they would win $1 million, according to officials.
    # Matching four numbers plus the “Mega Ball” would net the player $10,000. Matching four numbers without the “Mega Ball” would earn the player a $500 prize.
    # Matching three numbers and the “Mega Ball” is worth $200.
    # Matching three numbers, or matching two numbers and the “Mega Ball,” will win a player $10.
    # Matching one number and the “Mega Ball” is worth $4, and matching the “Mega Ball” is worth a $2 prize.
    regular_number_winner_count = 0
    mega_ball_winner_count = 0
    (regular_number_winners, mega_ball_winner) = get_number_matches_on_ticket(
        ticket=ticket,
        regular_winners=regular_winners,
        mega_ball_winner=mega_ball_winner,
    )
    # winning regular numbers
    # {"64": True, "12": True, "33": True, "19": True, "23": True}
    # winning mega ball number
    # {"12": True}
    for number in mega_ball_winner:
        if mega_ball_winner[number] == constants.MATCHED:
            mega_ball_winner_count += 1
    for number in regular_number_winners:
        if regular_number_winners[number] == constants.MATCHED:
            regular_number_winner_count += 1
    winnings = 0
    append = ""
    if mega_ball_winner_count >= 1:
        append = "mega"
        winnings = 2
    if regular_number_winner_count > 0:
        text = str(regular_number_winner_count) + "win" + append
        winnings = winning_options[text]
    return winnings


def calculate_cost_of_tickets(number_of_tickets: int, cost_of_ticket: int) -> int:
    return number_of_tickets * cost_of_ticket
