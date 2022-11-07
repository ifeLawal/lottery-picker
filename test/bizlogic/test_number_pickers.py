import unittest
from datetime import date

from bizlogic import constants
from bizlogic.number_pickers import (create_tickets, get_ordered_megaball,
                                     get_random_megaball,
                                     get_random_regular_numbers)


class TestNumberPickerMethods(unittest.TestCase):
    def test_random_created_tickets_are_unique(self) -> None:
        number_of_tickets = 30
        array_of_tickets = create_tickets(
            date=date.today(),
            number_of_tickets=number_of_tickets,
            get_regular_numbers=get_random_regular_numbers,
            generate_megaball=get_random_megaball,
        )
        # single ticket structure:
        # R - regular ball
        # M - mega ball
        #  R1, R2, R3, R4, R5, M1
        # [12, 32, 41, 23, 14, 12]

        set_of_tickets = set()
        for ticket in array_of_tickets:
            ticket_without_megaball = ticket[:-1]

            # convert tickets into frozensets
            # create a set from the frozensets
            frozen_set_ticket = frozenset(ticket_without_megaball)
            set_of_tickets.add(frozen_set_ticket)

        # check the length of tickets is still 30
        # this verifies that all the tickets are unique
        self.assertEqual(set_of_tickets.__len__(), number_of_tickets)

    def test_megaball_selections_are_in_order(self) -> None:
        number_of_tickets = 30
        array_of_tickets = create_tickets(
            date=date.today(),
            number_of_tickets=number_of_tickets,
            get_regular_numbers=get_random_regular_numbers,
            generate_megaball=get_ordered_megaball,
        )

        only_megaballs = []
        for ticket in array_of_tickets:
            only_megaballs.append(ticket[-1])

        counter = 1
        for i in range(number_of_tickets):
            assert counter == only_megaballs[i]
            counter = counter % constants.MEGA_BALL_MAX + 1


if __name__ == "__main__":
    unittest.main()
