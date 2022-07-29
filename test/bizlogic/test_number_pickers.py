from datetime import date
import unittest
from bizlogic import constants
from bizlogic.number_pickers import create_tickets, ordered_megaball, random_megaball, random_ticket_creation


class TestNumberPickerMethods(unittest.TestCase):
    def test_random_created_tickets_are_unique(self):
        number_of_tickets = 30
        array_of_tickets = create_tickets(date=date.today(), number_of_tickets=number_of_tickets, generate_tickets=random_ticket_creation, generate_megaball=random_megaball)
        
        set_of_tickets = set()
        for ticket in array_of_tickets:
            ticket_without_megaball = ticket[:-1]
            
            frozen_set_ticket = frozenset(ticket_without_megaball)
            set_of_tickets.add(frozen_set_ticket)
        
        self.assertEqual(set_of_tickets.__len__(), number_of_tickets)
    # convert tickets into frozensets
    # create a set from the frozensets
    # check the length is still 30
    
    # is each ticket an array or an object?
    # object - object structure {"first": 3, "second": 67, .., "fifth": 34, "megaball": 15}
    # vs
    # array - object structure [3, 67, .., 34, 15]
    # with array structure, if we sort the arrays we can quickly compare for duplicates
   # Verify that all the tickets are unique
    
    def test_megaball_ordered(self):
        number_of_tickets = 30
        array_of_tickets = create_tickets(date=date.today(), number_of_tickets=number_of_tickets, generate_tickets=random_ticket_creation, generate_megaball=ordered_megaball)
        
        only_megaballs = []
        for ticket in array_of_tickets:
            only_megaballs.append(ticket[-1])
        
        counter = 1
        for i in range(number_of_tickets):
            assert counter == only_megaballs[i]
            counter += 1
            if counter > constants.MEGA_BALL_MAX:
                counter = 1