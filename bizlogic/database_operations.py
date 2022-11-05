from datetime import date

from bizlogic import constants
from bizlogic.scrape_mega_millions import dao
from bizlogic.ticket_checker import (calculate_cost_of_tickets,
                                     check_winnings_for_a_ticket,
                                     check_winnings_for_multiple_tickets)


# ticket_type: Specify the type of tickets being generated
# tickets: list with the ticket numbers
def save_tickets_to_db(ticket_type: str, tickets: list) -> None:
    ins = dao.pure_random_ticket_attempts.insert()
    ins_config = dao.pure_random_configs.insert()

    if ticket_type == "random_regular_ordered_megaball":
        ins = dao.random_regular_ordered_megaball_ticket_attempts.insert()
        ins_config = dao.random_regular_ordered_megaball_configs.insert()
    for single_ticket in tickets:
        dao.connection.execute(
            ins,
            draw_date=date.today(),
            first_number=single_ticket[0],
            second_number=single_ticket[1],
            third_number=single_ticket[2],
            fourth_number=single_ticket[3],
            fifth_number=single_ticket[4],
            mega_ball=single_ticket[5],
            winnings=check_winnings_for_a_ticket(ticket=single_ticket, regular_winners={}, mega_ball_winner={})
            # TODO add Jackpot
        )
    total_wins = check_winnings_for_multiple_tickets(tickets=tickets, date=date.today())
    cost_of_tickets = calculate_cost_of_tickets(
        len(tickets), constants.COST_OF_MEGA_MILLIONS_TICKET
    )
    # TODO get the config row so we can get the current ticket spend and earnings
    # to update appropriately
    # with dao.session() as session:
    #     config = session.query(dao.r)

    dao.connection.execute(
        ins_config,
        total_ticket_spend=cost_of_tickets,
        total_ticket_earnings=total_wins
    )


def get_latest_winning_numbers() -> object:
    # I need to pull the latest winning row
    with dao.session() as session:
        winner = (
            session.query(dao.winners)
            .order_by(dao.winners.c.date.desc())  # TODO confirm this sort
            .first()
        )
        regular_number_wins = {
            str(winner.first_number): True,
            str(winner.second_number): True,
            str(winner.third_number): True,
            str(winner.fourth_number): True,
            str(winner.fifth_number): True,
        }
    return regular_number_wins, winner.jackpot, winner.megaball
