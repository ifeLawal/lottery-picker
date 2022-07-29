import datetime
import logging

from lxml import etree, html
# import json
from sqlalchemy.orm import sessionmaker

from bizlogic.date_mappings import days_of_the_week, months, quarters, years
from datastore.connecting import get_engine
from datastore.models.mega_millions import (Days, DaysOfTheWeek,
                                            MegaBallNumbers, Months, Quarters,
                                            RegularNumbers, Weeks, Winners,
                                            Years)
from datastore.models.mega_millions_generated_data import ConnectedNumberOccurrences
from scrape.scraper import Scraper

mega_millions_endpoint = "/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/index.html_2013354932.html"
table = "//div[@id='content']//table"
weeks_in_a_year = 52
days_in_a_month = 31

log = logging.getLogger(__name__)

row_mapper = {
    "date": 1,
    "numbers": 2,
    "mega_ball": 3,
    "megaplier": 4,
    "jackpot": 5,
    "winners": 6,
}

engine_name = "mega_millions_after_2013"
engine = get_engine(name=engine_name)
Session = sessionmaker(engine)
from datastore.models import create_all_tables, drop_all

if engine.has_table == False:
    create_all_tables(engine_name)
    log.log(1, "Table created")


def scrape_all_mega_millions_numbers() -> None:
    scraper = Scraper(base_url="https://www.texaslottery.com")
    # scraper.get_page_content(endpoint="/export/sites/lottery/Games/Mega_Millions/Winning_Numbers", inner_tag=table)
    drop_all(engine_name=engine_name)
    create_all_tables(engine_name=engine_name)
    create_date_mapping_tables()
    table = "//div[@id='content']//table//tbody/tr"
    rows = scraper.select_all_sections(endpoint=mega_millions_endpoint, xpath=table)
    for row in rows:
        hashmap = {}
        section_html_string = etree.tostring(row)
        section_root = html.fromstring(section_html_string)
        try:

            log.debug("Retrieving winning number data")
            for key, value in row_mapper.items():
                hashmap[key] = scraper.get_direct_text_from_element(
                    element=section_root, inner_tag=f"//td[position()={value}]"
                )
            log.debug("Retrieved winning number data")
        except Exception as ex:
            log.debug("Failed to retrieve winning number data")
            log.error(ex)
            log.debug("Continuing to run")
            continue
        numbers = parse_numbers(hashmap["numbers"])

        date_map = parse_date(hashmap["date"])
        if (
            date_map["year"] == 2013
            and date_map["month"] == 10
            and date_map["day"] == 18
        ):
            break
        with Session() as session:
            winner = Winners(
                draw_date=hashmap["date"],
                first_number=numbers[0],
                second_number=numbers[1],
                third_number=numbers[2],
                fourth_number=numbers[3],
                fifth_number=numbers[4],
                mega_ball=hashmap["mega_ball"],
                megaplier=hashmap["megaplier"],
                jackpot=hashmap["jackpot"],
            )
            session.add(winner)
            session.commit()

        for number in numbers:
            regular_numbers = RegularNumbers(
                number=number,
                month_id=date_map["month"],
                week_id=date_map["week"],
                quarter_id=date_map["quarter"],
                day_of_the_week_id=date_map["day_of_the_week"],
                year_id=years[date_map["year"]],
                day_id=date_map["day"],
            )
            session.add(regular_numbers)
            session.commit()

        mega_ball_number = MegaBallNumbers(
            number=hashmap["mega_ball"],
            month_id=date_map["month"],
            week_id=date_map["week"],
            quarter_id=date_map["quarter"],
            day_of_the_week_id=date_map["day_of_the_week"],
            year_id=years[date_map["year"]],
            day_id=date_map["day"],
        )
        session.add(mega_ball_number)
        session.commit()


def scrape_most_recent_mega_millions_number() -> None:
    scraper = Scraper(base_url="https://www.texaslottery.com")
    table = "//div[@id='content']//table//tbody/tr"
    rows = scraper.select_all_sections(endpoint=mega_millions_endpoint, xpath=table)
    counter = 0
    for row in rows:
        hashmap = {}
        section_html_string = etree.tostring(row)
        section_root = html.fromstring(section_html_string)
        try:

            log.debug("Retrieving winning number data")
            for key, value in row_mapper.items():
                hashmap[key] = scraper.get_direct_text_from_element(
                    element=section_root, inner_tag=f"//td[position()={value}]"
                )
            log.debug("Retrieved winning number data")
        except Exception as ex:
            log.debug("Failed to retrieve winning number data")
            log.error(ex)
            break
        numbers = parse_numbers(hashmap["numbers"])
        with Session() as session:
            winner = Winners(
                draw_date=hashmap["date"],
                first_number=numbers[0],
                second_number=numbers[1],
                third_number=numbers[2],
                fourth_number=numbers[3],
                fifth_number=numbers[4],
                mega_ball=hashmap["mega_ball"],
                megaplier=hashmap["megaplier"],
                jackpot=hashmap["jackpot"],
            )
            session.add(winner)
            session.commit()

        date_map = parse_date(hashmap["date"])
        for number in numbers:
            regular_numbers = RegularNumbers(
                number=number,
                month_id=date_map["month"],
                week_id=date_map["week"],
                quarter_id=date_map["quarter"],
                day_of_the_week_id=date_map["day_of_the_week"],
                year_id=years[date_map["year"]],
                day_id=date_map["day"],
            )
            session.add(regular_numbers)
            session.commit()

        mega_ball_number = MegaBallNumbers(
            number=hashmap["mega_ball"],
            month_id=date_map["month"],
            week_id=date_map["week"],
            quarter_id=date_map["quarter"],
            day_of_the_week_id=date_map["day_of_the_week"],
            year_id=years[date_map["year"]],
            day_id=date_map["day"],
        )
        session.add(mega_ball_number)
        session.commit()
        if counter >= 1:
            break
        counter += 1


def parse_date(date: str) -> object:
    date_mapper = {
        "month": 0,
        "week": 1,
        "quarter": 0,
        "day_of_the_week": 0,
        "year": 1,
        "day": 1,
    }
    format = "%m/%d/%Y"
    actual_date_format = datetime.datetime.strptime(date, format)
    date_mapper["day_of_the_week"] = actual_date_format.weekday()
    date_mapper["day"] = actual_date_format.day
    date_mapper["month"] = actual_date_format.month
    date_mapper["year"] = actual_date_format.year
    date_mapper["week"] = actual_date_format.isocalendar()[1]
    date_mapper["quarter"] = (actual_date_format.month - 1) // 3 + 1
    return date_mapper


def parse_numbers(numbers: str) -> list:
    final_numbers = []
    for number in numbers.split("-"):
        final_numbers.append(int(number.strip()))
    return final_numbers


def create_date_mapping_tables() -> None:
    with Session() as session:
        if session.query(Months.id).count() <=0 :
            for _, month in months.items():
                month = Months(month=month)
                session.add(month)
                session.commit()

        if session.query(DaysOfTheWeek.id).count() <=0 :
            for _, day_of_the_week in days_of_the_week.items():
                day_of_the_week = DaysOfTheWeek(day_of_the_week=day_of_the_week)
                session.add(day_of_the_week)
                session.commit()

        if session.query(Quarters.id).count() <=0 :
            for _, quarter in quarters.items():
                quarter = Quarters(quarter=quarter)
                session.add(quarter)
                session.commit()

        if session.query(Days.id).count() <=0 :
            for day in range(1, 32):
                day = Days(day=day)
                session.add(day)
                session.commit()

        if session.query(Weeks.id).count() <=0 :
            for week in range(1, 53):
                week = Weeks(week=week)
                session.add(week)
                session.commit()

        if session.query(Years.id).count() <=0 :
            for year, _ in years.items():
                year = Years(year=year)
                session.add(year)
                session.commit()

        if session.query(ConnectedNumberOccurrences.id).count() <=0:
            for numbers_possible in range(1, 71):
                connectedNumberOccurrences = ConnectedNumberOccurrences(lottery_number=numbers_possible)
                session.add(connectedNumberOccurrences)
                session.commit()