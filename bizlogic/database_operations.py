from sqlalchemy import Date
from sqlalchemy.sql import func, select, update

from bizlogic import constants
from bizlogic.scrape_mega_millions import dao
from bizlogic.ticket_checker import (calculate_cost_of_tickets,
                                     check_winnings_for_a_mega_millions_ticket,
                                     check_winnings_for_multiple_tickets)


# Product use: save tickets we are generating the day before the drawing
# ticket_type: Specify the type of tickets being generated
# tickets: list with the ticket numbers
def save_tickets_to_db(ticket_type: str, tickets: list, date: Date) -> None:
    ins = dao.pure_random_ticket_attempts.insert()

    if ticket_type == "random_regular_ordered_megaball":
        ins = dao.random_regular_ordered_megaball_ticket_attempts.insert()

    for single_ticket in tickets:
        dao.connection.execute(
            ins,
            draw_date=date,
            first_number=single_ticket[0],
            second_number=single_ticket[1],
            third_number=single_ticket[2],
            fourth_number=single_ticket[3],
            fifth_number=single_ticket[4],
            mega_ball=single_ticket[5],
        )


# If a date is given, use it
# otherwise go for today
def update_winnings(ticket_type: str, draw_date: Date = None) -> object:
    winning_ticket_date = ""
    guessed_ticket_date = ""
    winner = ""
    if draw_date == None:
        # If no draw_date given, get the latest winner ticket and latest guessed ticket and use that to compare
        with dao.session() as session:
            winner = (
                session.query(dao.winners)
                .order_by(dao.winners.c.draw_date.desc())
                .first()
            )
            # TODO use the ticket_type to change which db we select from
            guessed = (
                session.query(dao.pure_random_ticket_attempts)
                .order_by(dao.pure_random_ticket_attempts.c.draw_date.desc())
                .first()
            )
        winning_ticket_date = winner.draw_date
        guessed_ticket_date = guessed.draw_date
    else:
        winning_ticket_date = guessed_ticket_date = draw_date

    tickets = get_tickets_played(guessed_ticket_date)
    config_row = update_winnings_of_our_tickets(
        tickets=tickets, ticket_type=ticket_type, draw_date=winning_ticket_date
    )
    return winner, config_row


def update_winnings_of_our_tickets(
    tickets: list, ticket_type: str, draw_date: Date
) -> object:
    configs_columns_to_select = select(
        [
            dao.pure_random_configs.c.total_ticket_spend,
            dao.pure_random_configs.c.total_ticket_earnings,
            dao.pure_random_configs.c.biggest_win,
        ]
    )

    (
        regular_number_wins,
        jackpot,
        megaball_number_win,
        draw_date,
    ) = get_winning_numbers(draw_date)

    # tickets = get_tickets_played(date_str)
    # winnings=check_winnings_for_a_ticket(
    #             ticket=single_ticket, regular_winners=regular_number_wins, mega_ball_winner=megaball_number_win
    #         ),
    #         jackpot=jackpot

    if ticket_type == "random_regular_ordered_megaball":
        configs_columns_to_select = select(
            [
                dao.random_regular_ordered_megaball_configs.c.total_ticket_spend,
                dao.random_regular_ordered_megaball_configs.c.total_ticket_earnings,
                dao.random_regular_ordered_megaball_configs.c.biggest_win,
            ]
        )

    for single_ticket in tickets:
        update_columns = update(dao.pure_random_ticket_attempts).where(
            dao.pure_random_ticket_attempts.c.id == single_ticket.id
        )
        update_statement = update_columns.values(
            winnings=check_winnings_for_a_mega_millions_ticket(
                ticket=single_ticket,
                regular_winners=regular_number_wins,
                mega_ball_winner=megaball_number_win,
            ),
            jackpot=jackpot,
            numbers_that_matched=0,
            amt_of_numbers_that_matched=0,
        )
        dao.connection.execute(update_statement)

    total_wins = check_winnings_for_multiple_tickets(tickets=tickets, date=draw_date)

    config_row = dao.connection.execute(configs_columns_to_select).first()
    with dao.session() as session:
        cost_of_all_tickets = calculate_cost_of_tickets(
            session.query(dao.pure_random_ticket_attempts).count(),
            constants.COST_OF_MEGA_MILLIONS_TICKET,
        )
        winnings_of_all_tickets = session.query(
            func.sum(dao.pure_random_ticket_attempts.c.winnings)
        ).scalar()

    if config_row == None:
        if ticket_type == "random":
            ins = dao.pure_random_configs.insert()
        elif ticket_type == "weighted":
            ins = dao.weighted_configs.insert()

        dao.connection.execute(
            ins,
            total_ticket_spend=cost_of_all_tickets,
            total_ticket_earnings=winnings_of_all_tickets,
            biggest_win=total_wins,
        )
    else:
        update_columns = update(dao.pure_random_configs).where(
            dao.pure_random_configs.c.id == 1
        )

        biggest_win = total_wins
        # TODO figure out if I want biggest win by ticket or by date.
        # current form is by date
        # save the biggest win. Might have to move this to the check winnings section
        if config_row.biggest_win > total_wins:
            biggest_win = config_row.biggest_win

        update_config = update_columns.values(
            total_ticket_spend=cost_of_all_tickets,
            total_ticket_earnings=winnings_of_all_tickets,
            biggest_win=biggest_win,
        )

        dao.connection.execute(update_config)

    config_row = dao.connection.execute(configs_columns_to_select).first()
    return config_row


# Get winning numbers for a given date
# or if no date given get the latest winning numbers
def get_winning_numbers(draw_date: Date = None) -> object:
    # I need to pull the latest winning row
    with dao.session() as session:
        if draw_date == None:
            winner = (
                session.query(dao.winners)
                # TODO confirm this sort
                .order_by(dao.winners.c.draw_date.desc()).first()
            )
        else:
            winner = (
                session.query(dao.winners)
                .filter(dao.winners.c.draw_date == draw_date)
                .first()
            )
        regular_number_wins = {
            str(winner.first_number): True,
            str(winner.second_number): True,
            str(winner.third_number): True,
            str(winner.fourth_number): True,
            str(winner.fifth_number): True,
        }
        megeball_number_wins = {str(winner.mega_ball): True}

    return regular_number_wins, winner.jackpot, megeball_number_wins, winner.draw_date


def get_tickets_played(draw_date: Date, order_by: str = None) -> list:
    tickets = []
    with dao.session() as session:
        query = session.query(dao.pure_random_ticket_attempts).filter(
            dao.pure_random_ticket_attempts.c.draw_date == draw_date
        )
        if order_by:
            tickets = query.order_by(
                dao.pure_random_ticket_attempts.c[order_by].desc()
            ).all()
        else:
            tickets = query.all()
    return tickets
