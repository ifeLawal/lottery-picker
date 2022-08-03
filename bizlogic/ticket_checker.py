from datetime import date
from bizlogic import constants
from bizlogic.mega_millions import Session
from datastore.models.mega_millions import Winners

def check_list_of_tickets(ticket: list, date: date):
    draw_date = "07/26/22"
    with Session() as session:
        winner = session.query(Winners).filter(Winners.draw_date == draw_date)
        # winning_ticket = {str(winner.first_number):""} [, winner.second_number, winner.third_number, winner.fourth_number, winner.fifth_number, winner.mega_ball]
        # 
        
    return [{constants.REGULAR_NUMBERS_PROPERTY_NAME:{"23": constants.MATCHED, "43": constants.UNMATCHED}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: {"23"}}]

def get_number_matches_on_ticket(ticket: list, regular_winners: object, mega_ball_winner: object) -> object:
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
    return {constants.REGULAR_NUMBERS_PROPERTY_NAME: regular_number_results, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: mega_ball_number_results}

"""
ticket_matching expected sample object
{"regular_numbers":{"23": "match found", "43": "no match", "56": "no match", "1": "no match", "10": "no match"}, "mega_ball_number": {"23": "match found"}}]
"""
def check_winnings_for_a_ticket(ticket_matching: object) -> int:
    # If a player matches all five numbers, but not the “Mega Ball,” then they would win $1 million, according to officials.
    # Matching four numbers plus the “Mega Ball” would net the player $10,000. Matching four numbers without the “Mega Ball” would earn the player a $500 prize.
    # Matching three numbers and the “Mega Ball” is worth $200.
    # Matching three numbers, or matching two numbers and the “Mega Ball,” will win a player $10.
    # Matching one number and the “Mega Ball” is worth $4, and matching the “Mega Ball” is worth a $2 prize.
    regular_number_winners = 0
    mega_ball_match = 0
    regular_numbers = ticket_matching[constants.REGULAR_NUMBERS_PROPERTY_NAME]
    mega_ball_number = ticket_matching[constants.MEGA_BALL_NUMBER_PROPERTY_NAME]
    for mega_ball in ticket_matching[constants.MEGA_BALL_NUMBER_PROPERTY_NAME]:
        # if mega_ball[]
        pass
    for regular_numbers in ticket_matching[constants.REGULAR_NUMBERS_PROPERTY_NAME]:
        pass    
        
    return 0