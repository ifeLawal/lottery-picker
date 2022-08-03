from datetime import date
import unittest
from bizlogic import constants
from bizlogic.number_pickers import create_tickets, ordered_megaball, random_megaball, random_ticket_creation
from bizlogic.ticket_checker import get_number_matches_on_ticket

sample_winning_ticket_list = [64, 12, 33, 19, 23, 12]
# sample_winning_ticket_obj = {constants.REGULAR_NUMBERS_PROPERTY_NAME: {"64": True, "12": True, "33": True, "19": True, "23": True}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME:{"12": True}}
sample_regular_winning_ticket = {"64": True, "12": True, "33": True, "19": True, "23": True}
sample_winning_mega_ball = {"12": True}
sample_guess_ticket = [23, 45, 64, 12, 43, 23]

class TestTicketCheckerMethods(unittest.TestCase):
    def test_single_ticket_matching(self) -> None:
        # {constants.REGULAR_NUMBERS_PROPERTY_NAME:{"23":constants.MATCHED,"45":constants.UNMATCHED,"64":constants.MATCHED,"12":constants.MATCHED,"43":constants.UNMATCHED}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: {"23":constants.UNMATCHED}}
        expected_regular_number_result = {"23":constants.MATCHED,"45":constants.UNMATCHED,"64":constants.MATCHED,"12":constants.MATCHED,"43":constants.UNMATCHED}
        expected_mega_ball_number_result = {"23":constants.UNMATCHED}
        
        actual_matching_results = get_number_matches_on_ticket(sample_guess_ticket,sample_regular_winning_ticket,sample_winning_mega_ball)
        
        regular_numbers_match = actual_matching_results[constants.REGULAR_NUMBERS_PROPERTY_NAME]
        print(regular_numbers_match)
        mega_ball_number_match = actual_matching_results[constants.MEGA_BALL_NUMBER_PROPERTY_NAME]
        print(mega_ball_number_match)
        for number in regular_numbers_match:
            assert expected_regular_number_result[number] == regular_numbers_match[number]
        for mega_ball in mega_ball_number_match:
            assert expected_mega_ball_number_result[mega_ball] == mega_ball_number_match[mega_ball]
        