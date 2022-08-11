from datetime import date
from bizlogic import constants
from bizlogic.mega_millions import Session
from datastore.models.mega_millions import Winners

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
    "mega": 2
}

def check_list_of_tickets(ticket: list, date: date):
    draw_date = "07/26/22"
    with Session() as session:
        winner = session.query(Winners).filter(Winners.draw_date == draw_date)
        # winning_ticket = {str(winner.first_number):""} [, winner.second_number, winner.third_number, winner.fourth_number, winner.fifth_number, winner.mega_ball]
        # 
        
    return [{constants.REGULAR_NUMBERS_PROPERTY_NAME:{"23": constants.MATCHED, "43": constants.UNMATCHED}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: {"23"}}]

def get_number_matches_on_ticket(ticket: list, regular_winners: object, mega_ball_winner: object) -> object:
    """
    :return: regular number matches and mega ball matches
    :rtype: tuple sample - ({"64": True, "12": True, "33": True, "19": True, "23": True}, {"12": True})
    """
    regular_number_results = {}
    mega_ball_number_results = {}
    counter = 0
    # tickets are 6 length arrays: 5 regular and 1 mega ball
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
    # return {constants.REGULAR_NUMBERS_PROPERTY_NAME: regular_number_results, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: mega_ball_number_results}

def check_winnings_for_a_ticket(ticket: list, regular_winners: object, mega_ball_winner: object) -> int:
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
    (regular_number_winners, mega_ball_winner) = get_number_matches_on_ticket(ticket=ticket, regular_winners=regular_winners, mega_ball_winner=mega_ball_winner)
    for number in mega_ball_winner:
        if mega_ball_winner[number] == constants.MATCHED:
            mega_ball_winner_count += 1
            print("we got the mega ball")
    for number in regular_number_winners:
        if regular_number_winners[number] == constants.MATCHED:
            regular_number_winner_count += 1
    winnings = 0
    append = ""
    if mega_ball_winner_count >= 1:
        append = "mega"
        winnings = 2
    if regular_number_winner_count == 5:
        return winning_options["5win"+append]
    if regular_number_winner_count == 4:
        return winning_options["4win"+append]
    if regular_number_winner_count == 3:
        return winning_options["3win"+append]
    if regular_number_winner_count == 2:
        return winning_options["2win"+append]
    if regular_number_winner_count == 1:
        return winning_options["1win"+append]

    return winnings