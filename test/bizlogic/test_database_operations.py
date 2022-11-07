import unittest
from datetime import date
from sqlalchemy.sql import select, update

from bizlogic.database_operations import get_latest_winning_numbers, save_tickets_to_db
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

    def test_latest_winning_numbers(self) -> None:
        (regular_number_wins, jackpot, megaball,
         draw_date) = get_latest_winning_numbers()
        print(regular_number_wins)
        print(jackpot)
        print(megaball)
        print(draw_date)
        columns = [
            dao.pure_random_configs.c.id,
            dao.pure_random_configs.c.total_ticket_spend,
            dao.pure_random_configs.c.total_ticket_earnings,
            dao.pure_random_configs.c.biggest_win]
        select_configs = select(columns)
        update_columns = update(dao.pure_random_configs).where(
            dao.pure_random_configs.c.id == 1)
        config_row = dao.connection.execute(select_configs).first()
        print(config_row)
        update_config = update_columns.values(
            total_ticket_spend=config_row.total_ticket_spend + 30,
            total_ticket_earnings=config_row.total_ticket_earnings + 10,
        )
        dao.connection.execute(update_config)
        print(dao.connection.execute(select_configs).first())
        assert draw_date == "07/28/2022"


if __name__ == "__main__":
    unittest.main()
