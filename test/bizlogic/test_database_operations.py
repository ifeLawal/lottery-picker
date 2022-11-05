import unittest
from datetime import date

from bizlogic.database_operations import save_tickets_to_db
from bizlogic.number_pickers import (create_tickets, get_ordered_megaball,
                                     get_random_regular_numbers)
from datastore.models.mega_millions import dao, prep_db


class TestNumberPickerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dao.db_init("sqlite:///:memory:")
        prep_db()

    def test_save_to_db(self) -> None:
        number_of_tickets = 30
        array_of_tickets = create_tickets(
            date=date.today(),
            number_of_tickets=number_of_tickets,
            get_regular_numbers=get_random_regular_numbers,
            generate_megaball=get_ordered_megaball,
        )

        save_tickets_to_db(ticket_type="random", tickets=array_of_tickets)

if __name__ == '__main__':
    unittest.main()