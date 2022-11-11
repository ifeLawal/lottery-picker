from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.orm import sessionmaker

from bizlogic.date_mappings import days_of_the_week, months, quarters, years

weeks_in_a_year = 52
days_in_a_month = 31


class DataAccessObject:
    connection = None
    engine = None
    conn_string = None
    session = None
    metadata = MetaData()
    winners = Table(
        "winners",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("draw_date", String(128), nullable=False),
        Column("first_number", Integer()),
        Column("second_number", Integer()),
        Column("third_number", Integer()),
        Column("fourth_number", Integer()),
        Column("fifth_number", Integer()),
        Column("mega_ball", Integer()),
        Column("megaplier", Integer()),
        Column("jackpot", String(128)),
    )

    regular_numbers = Table(
        "regular_numbers",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("number", Integer(), nullable=False),
        Column("month_id", Integer(), ForeignKey("months.id"), nullable=False),
        Column("week_id", Integer(), ForeignKey("weeks.id"), nullable=False),
        Column("quarter_id", Integer(), ForeignKey("quarters.id"), nullable=False),
        Column(
            "day_of_the_week_id",
            Integer(),
            ForeignKey("days_of_the_week.id"),
            nullable=False,
        ),
        Column("year_id", Integer(), ForeignKey("years.id"), nullable=False),
        Column("day_id", Integer(), ForeignKey("days.id"), nullable=False),
    )

    mega_ball_numbers = Table(
        "mega_ball_numbers",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("number", Integer(), nullable=False),
        Column("month_id", Integer(), ForeignKey("months.id"), nullable=False),
        Column("week_id", Integer(), ForeignKey("weeks.id"), nullable=False),
        Column("quarter_id", Integer(), ForeignKey("quarters.id"), nullable=False),
        Column(
            "day_of_the_week_id",
            Integer(),
            ForeignKey("days_of_the_week.id"),
            nullable=False,
        ),
        Column("year_id", Integer(), ForeignKey("years.id"), nullable=False),
        Column("day_id", Integer(), ForeignKey("days.id"), nullable=False),
    )

    months = Table(
        "months",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("month", String(128), nullable=False),
    )

    days_of_the_week = Table(
        "days_of_the_week",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("day_of_the_week", String(128), nullable=False),
    )

    weeks = Table(
        "weeks",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("week", Integer(), nullable=False),
    )

    quarters = Table(
        "quarters",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("quarter", String(128), nullable=False),
    )

    years = Table(
        "years",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("year", Integer(), nullable=False),
    )

    days = Table(
        "days",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("day", Integer(), nullable=False),
    )

    pure_random_ticket_attempts = Table(
        "pure_random_ticket_attempts",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("draw_date", String(128), nullable=False),
        Column("first_number", Integer()),
        Column("second_number", Integer()),
        Column("third_number", Integer()),
        Column("fourth_number", Integer()),
        Column("fifth_number", Integer()),
        Column("mega_ball", Integer()),
        Column("numbers_that_matched", String(128)),
        Column("amt_of_numbers_that_matched", Integer()),
        Column("winnings", Integer()),
        Column("jackpot", String(128)),
    )

    pure_random_configs = Table(
        "pure_random_configs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("total_ticket_spend", Integer, default=0),
        Column("total_ticket_earnings", Integer, default=0),
        Column("biggest_win", Integer, default=0),
    )

    random_regular_ordered_megaball_ticket_attempts = Table(
        "random_regular_ordered_megaball_ticket_attempts",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("draw_date", String(128), nullable=False),
        Column("first_number", Integer()),
        Column("second_number", Integer()),
        Column("third_number", Integer()),
        Column("fourth_number", Integer()),
        Column("fifth_number", Integer()),
        Column("mega_ball", Integer()),
        Column("numbers_that_matched", String(128)),
        Column("amt_of_numbers_that_matched", Integer()),
        Column("winnings", Integer()),
        Column("jackpot", String(128)),
    )

    random_regular_ordered_megaball_configs = Table(
        "random_regular_ordered_megaball_configs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("total_ticket_spend", Integer, default=0),
        Column("total_ticket_earnings", Integer, default=0),
        Column("biggest_win", Integer, default=0),
    )

    weighted_ticket_attempts = Table(
        "weighted_ticket_attempts",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("draw_date", String(128), nullable=False),
        Column("first_number", Integer()),
        Column("second_number", Integer()),
        Column("third_number", Integer()),
        Column("fourth_number", Integer()),
        Column("fifth_number", Integer()),
        Column("mega_ball", Integer()),
        Column("numbers_that_matched", String(128)),
        Column("amt_that_matched", Integer()),
        Column("jackpot", String(128)),
    )

    weighted_configs = Table(
        "weighted_configs",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("total_ticket_spend", Integer, default=0),
        Column("total_ticket_earnings", Integer, default=0),
        Column("biggest_win", Integer, default=0),
    )

    connected_number_occurrences = Table(
        "connected_number_occurrences",
        metadata,
        Column("id", Integer(), primary_key=True),
        Column("lottery_number", Integer(), nullable=False),
        Column("Number1", Integer(), default=0),
        Column("Number2", Integer(), default=0),
        Column("Number3", Integer(), default=0),
        Column("Number4", Integer(), default=0),
        Column("Number5", Integer(), default=0),
        Column("Number6", Integer(), default=0),
        Column("Number7", Integer(), default=0),
        Column("Number8", Integer(), default=0),
        Column("Number9", Integer(), default=0),
        Column("Number10", Integer(), default=0),
        Column("Number11", Integer(), default=0),
        Column("Number12", Integer(), default=0),
        Column("Number13", Integer(), default=0),
        Column("Number14", Integer(), default=0),
        Column("Number15", Integer(), default=0),
        Column("Number16", Integer(), default=0),
        Column("Number17", Integer(), default=0),
        Column("Number18", Integer(), default=0),
        Column("Number19", Integer(), default=0),
        Column("Number20", Integer(), default=0),
        Column("Number21", Integer(), default=0),
        Column("Number22", Integer(), default=0),
        Column("Number23", Integer(), default=0),
        Column("Number24", Integer(), default=0),
        Column("Number25", Integer(), default=0),
        Column("Number26", Integer(), default=0),
        Column("Number27", Integer(), default=0),
        Column("Number28", Integer(), default=0),
        Column("Number29", Integer(), default=0),
        Column("Number30", Integer(), default=0),
        Column("Number31", Integer(), default=0),
        Column("Number32", Integer(), default=0),
        Column("Number33", Integer(), default=0),
        Column("Number34", Integer(), default=0),
        Column("Number35", Integer(), default=0),
        Column("Number36", Integer(), default=0),
        Column("Number37", Integer(), default=0),
        Column("Number38", Integer(), default=0),
        Column("Number39", Integer(), default=0),
        Column("Number40", Integer(), default=0),
        Column("Number41", Integer(), default=0),
        Column("Number42", Integer(), default=0),
        Column("Number43", Integer(), default=0),
        Column("Number44", Integer(), default=0),
        Column("Number45", Integer(), default=0),
        Column("Number46", Integer(), default=0),
        Column("Number47", Integer(), default=0),
        Column("Number48", Integer(), default=0),
        Column("Number49", Integer(), default=0),
        Column("Number50", Integer(), default=0),
        Column("Number51", Integer(), default=0),
        Column("Number52", Integer(), default=0),
        Column("Number53", Integer(), default=0),
        Column("Number54", Integer(), default=0),
        Column("Number55", Integer(), default=0),
        Column("Number56", Integer(), default=0),
        Column("Number57", Integer(), default=0),
        Column("Number58", Integer(), default=0),
        Column("Number59", Integer(), default=0),
        Column("Number60", Integer(), default=0),
        Column("Number61", Integer(), default=0),
        Column("Number62", Integer(), default=0),
        Column("Number63", Integer(), default=0),
        Column("Number64", Integer(), default=0),
        Column("Number65", Integer(), default=0),
        Column("Number66", Integer(), default=0),
        Column("Number67", Integer(), default=0),
        Column("Number68", Integer(), default=0),
        Column("Number69", Integer(), default=0),
        Column("Number70", Integer(), default=0),
    )

    def set_conn_string(self, conn_string) -> None:
        self.conn_string = conn_string

    def db_init(self, conn_string) -> None:
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)

    def db_drop_table(self, table: str) -> None:
        self.metadata.tables[table].drop(self.engine)

    def reset_table(self, table: str) -> None:
        self.metadata.tables[table].drop(self.engine)
        self.metadata.tables[table].create(self.engine)

    def db_drop_all(self) -> None:
        self.engine = create_engine(self.conn_string)
        self.metadata.drop_all(self.engine)
        self.connection = self.engine.connect()

    def get_engine(self) -> engine:
        return self.engine


dao = DataAccessObject()


def prep_db() -> None:
    ins = dao.regular_numbers.insert()
    dao.connection.execute(
        ins,
        number=23,
        month_id=3,
        week_id=4,
        quarter_id=1,
        day_of_the_week_id=2,
        year_id=2,
        day_id=2,
    )
    regular_numbers_list = [
        {
            "number": 14,
            "month_id": 12,
            "week_id": 3,
            "quarter_id": 2,
            "day_of_the_week_id": 1,
            "year_id": 3,
            "day_id": 10,
        },
        {
            "number": 28,
            "month_id": 7,
            "week_id": 5,
            "quarter_id": 3,
            "day_of_the_week_id": 6,
            "year_id": 4,
            "day_id": 7,
        },
    ]
    dao.connection.execute(ins, regular_numbers_list)

    ins = dao.winners.insert()
    winners_list = [
        {
            "draw_date": "07/26/2022",
            "first_number": "64",
            "second_number": "12",
            "third_number": "33",
            "fourth_number": "19",
            "fifth_number": "23",
            "mega_ball": "12",
            "megaplier": "2",
            "jackpot": "$82 million",
        },
        {
            "draw_date": "07/28/2022",
            "first_number": "14",
            "second_number": "17",
            "third_number": "9",
            "fourth_number": "28",
            "fifth_number": "50",
            "mega_ball": "7",
            "megaplier": "2",
            "jackpot": "$109 million",
        },
    ]
    dao.connection.execute(ins, winners_list)

    ins = dao.pure_random_configs.insert()

    configs_items = [
        {"total_ticket_spend": 0, "total_ticket_earnings": 0, "biggest_win": 0}
    ]
    dao.connection.execute(ins, configs_items)


"""
Create support tables meant for number analysis
"""


def create_date_mapping_tables() -> None:
    ins = dao.months.insert()
    for _, month in months.items():
        dao.connection.execute(ins, month=month)

    ins = dao.days_of_the_week.insert()
    for _, day_of_the_week in days_of_the_week.items():
        dao.connection.execute(ins, day_of_the_week=day_of_the_week)

    ins = dao.quarters.insert()
    for _, quarter in quarters.items():
        dao.connection.execute(ins, quarter=quarter)

    ins = dao.days.insert()
    for day in range(1, days_in_a_month + 1):
        dao.connection.execute(ins, day=day)

    ins = dao.weeks.insert()
    for week in range(1, weeks_in_a_year + 1):
        dao.connection.execute(ins, week=week)

    ins = dao.years.insert()
    for year, _ in years.items():
        dao.connection.execute(ins, year=year)

    ins = dao.connected_number_occurrences.insert()
    for numbers_possible in range(1, 71):
        dao.connection.execute(ins, lottery_number=numbers_possible)

    # TODO - create DaysAgo table
