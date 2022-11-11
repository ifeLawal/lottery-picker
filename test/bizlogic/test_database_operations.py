import unittest
from datetime import date

from sqlalchemy.sql import select, update

from bizlogic.database_operations import (get_tickets_played, get_winning_numbers,
                                          save_tickets_to_db, update_winnings,
                                          update_winnings_of_our_tickets)
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
            number_of_tickets=number_of_tickets,
            get_regular_numbers=get_random_regular_numbers,
            generate_megaball=get_ordered_megaball,
        )

        draw_date = "07/26/2022"
        save_tickets_to_db(
            ticket_type="random", tickets=array_of_tickets, date=draw_date
        )
        tickets = []
        with dao.session() as session:
            tickets = (
                session.query(dao.pure_random_ticket_attempts)
                .filter(dao.pure_random_ticket_attempts.c.draw_date == draw_date)
                .all()
            )
        print(tickets)
        print(tickets[0].id)
        assert len(tickets) == number_of_tickets

    def test_winning_numbers(self) -> None:
        (
            regular_number_wins,
            jackpot,
            megaball,
            draw_date,
        ) = get_winning_numbers()
        # print(regular_number_wins)
        # print(jackpot)
        # print(megaball)
        # print(draw_date)
        columns = [
            dao.pure_random_configs.c.id,
            dao.pure_random_configs.c.total_ticket_spend,
            dao.pure_random_configs.c.total_ticket_earnings,
            dao.pure_random_configs.c.biggest_win,
        ]
        select_configs = select(columns)
        update_columns = update(dao.pure_random_configs).where(
            dao.pure_random_configs.c.id == 1
        )
        config_row = dao.connection.execute(select_configs).first()
        # print(config_row)
        update_config = update_columns.values(
            total_ticket_spend=config_row.total_ticket_spend + 30,
            total_ticket_earnings=config_row.total_ticket_earnings + 10,
        )
        dao.connection.execute(update_config)
        # print(dao.connection.execute(select_configs).first())
        assert draw_date == "07/28/2022"

    def test_update_latest_winnings(self) -> None:

        configs_columns_to_select = select(
        [
            dao.pure_random_configs.c.total_ticket_spend,
            dao.pure_random_configs.c.total_ticket_earnings,
            dao.pure_random_configs.c.biggest_win,
            ]
        )
        config_row = dao.connection.execute(configs_columns_to_select).first()
        print(config_row)
        print("==============================")
        number_of_tickets = 30
        array_of_tickets = create_tickets(
            number_of_tickets=number_of_tickets,
            get_regular_numbers=get_random_regular_numbers,
            generate_megaball=get_ordered_megaball,
        )

        draw_date = "07/26/2022"
        print("len(tickets_played): " + str(len(get_tickets_played(draw_date))))
        update_winnings(ticket_type="random", draw_date=draw_date)
        print(get_tickets_played(draw_date, "winnings"))
        

        print("==============================")
        config_row = dao.connection.execute(configs_columns_to_select).first()
        print(config_row)
        


if __name__ == "__main__":
    unittest.main()
