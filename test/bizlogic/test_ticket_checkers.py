from datetime import date
import unittest
from bizlogic import constants
from bizlogic.number_pickers import (
    create_tickets,
    ordered_megaball,
    random_megaball,
    random_ticket_creation,
)
from bizlogic.ticket_checker import (
    check_winnings_for_a_ticket,
    get_number_matches_on_ticket,
    check_winnings_for_multiple_tickets
)
from datastore.models.mega_millions import dao, prep_db

# sample_winning_ticket_obj = {constants.REGULAR_NUMBERS_PROPERTY_NAME: {"64": True, "12": True, "33": True, "19": True, "23": True}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME:{"12": True}}
sample_winning_ticket = [64, 12, 33, 19, 23, 12]
sample_regular_winning_ticket = {
    "64": True,
    "12": True,
    "33": True,
    "19": True,
    "23": True,
}
sample_winning_mega_ball = {"12": True}
sample_guess_ticket = [23, 45, 64, 12, 43, 23]
sample_guess_multiple_tickets = [[23, 45, 64, 12, 43, 23],[23, 1, 55, 89, 30, 12], [22, 1, 55, 89, 30, 12],[23, 1, 55, 89, 30, 22]]


class TestTicketCheckerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dao.db_init("sqlite:///:memory:")
        prep_db()

    def test_single_ticket_matching(self) -> None:
        # {constants.REGULAR_NUMBERS_PROPERTY_NAME:{"23":constants.MATCHED,"45":constants.UNMATCHED,"64":constants.MATCHED,"12":constants.MATCHED,"43":constants.UNMATCHED}, constants.MEGA_BALL_NUMBER_PROPERTY_NAME: {"23":constants.UNMATCHED}}
        expected_regular_number_result = {
            "23": constants.MATCHED,
            "45": constants.UNMATCHED,
            "64": constants.MATCHED,
            "12": constants.MATCHED,
            "43": constants.UNMATCHED,
        }
        expected_mega_ball_number_result = {"23": constants.UNMATCHED}

        (regular_numbers_match, mega_ball_number_match) = get_number_matches_on_ticket(
            sample_guess_ticket, sample_regular_winning_ticket, sample_winning_mega_ball
        )

        print(regular_numbers_match)
        print(mega_ball_number_match)
        for number in regular_numbers_match:
            assert (
                expected_regular_number_result[number] == regular_numbers_match[number]
            )
        for mega_ball in mega_ball_number_match:
            assert (
                expected_mega_ball_number_result[mega_ball]
                == mega_ball_number_match[mega_ball]
            )

    def test_check_winnings(self) -> None:
        expected = 10
        actual = check_winnings_for_a_ticket(
            ticket=sample_guess_ticket,
            regular_winners=sample_regular_winning_ticket,
            mega_ball_winner=sample_winning_mega_ball,
        )

        assert expected == actual

    def test_check_winnings_for_multiple_tickets(self) -> None:
        expected = 16
        actual = check_winnings_for_multiple_tickets(tickets=sample_guess_multiple_tickets, date="07/26/2022")
        
        assert expected == actual
    
    def test_create_tickets_and_check_for_wins(self) -> None:
        expected = 0
        tickets = create_tickets(date="", number_of_tickets=60, generate_tickets=random_ticket_creation, generate_megaball=ordered_megaball)
        actual = check_winnings_for_multiple_tickets(tickets=tickets, date="07/26/2022")
        print(actual)
        assert expected == actual