import datetime
import logging

from lxml import etree, html

from bizlogic.date_mappings import years
from datastore.connecting import DatabaseConnector
from datastore.models.mega_millions import create_date_mapping_tables
from scrape.scraper import Scraper

# import json


mega_millions_endpoint = "/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/index.html_2013354932.html"
table = "//div[@id='content']//table"

log = logging.getLogger(__name__)

row_mapper = {
    "date": 1,
    "numbers": 2,
    "mega_ball": 3,
    "megaplier": 4,
    "jackpot": 5,
    "winners": 6,
}

# engine_name = "mega_millions_after_2013"
engine_name = "mega_millions_test_dao"
dbconnect = DatabaseConnector()
dao = dbconnect.get_data_access_object(name=engine_name)

# if engine.has_table == False:
#     create_all_tables(engine_name)
#     log.log(1, "Table created")


def scrape_all_mega_millions_numbers() -> None:
    scraper = Scraper(base_url="https://www.texaslottery.com")
    # scraper.get_page_content(endpoint="/export/sites/lottery/Games/Mega_Millions/Winning_Numbers", inner_tag=table)
    dao = dbconnect.clean_tables_and_get_data_access_object(name=engine_name)
    create_date_mapping_tables()
    table = "//div[@id='content']//table//tbody/tr"
    # full website link: https://www.texaslottery.com/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/index.html_2013354932.html
    rows = scraper.select_all_sections(endpoint=mega_millions_endpoint, xpath=table)

    for row in rows:
        hashmap = {}
        section_html_string = etree.tostring(row)
        section_root = html.fromstring(section_html_string)
        # As a note this fails because the mega millions changed up lottery matrices a few times.
        # The times are: 10/31/2017, 10/22/2013, 6/24/2005
        try:
            log.debug("Retrieving winning number data")
            for key, value in row_mapper.items():
                hashmap[key] = scraper.get_direct_text_from_element(
                    element=section_root, inner_tag=f"//td[position()={value}]"
                )
            log.debug("Retrieved winning number data")
        except Exception as ex:
            print(f"Error {ex}")
            log.debug("Failed to retrieve winning number data")
            log.error(ex)
            break
        numbers = parse_numbers(hashmap["numbers"])

        date_map = parse_date(hashmap["date"])
        # This was if we wanted to go all the way to the 2013 lottery drawing type
        # if (
        #     date_map["year"] == 2013
        #     and date_map["month"] == 10
        #     and date_map["day"] == 18
        # ):
        #     break
        ins = dao.winners.insert()
        dao.connection.execute(
            ins,
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

        ins = dao.regular_numbers.insert()
        for number in numbers:
            dao.connection.execute(
                ins,
                number=number,
                month_id=date_map["month"],
                week_id=date_map["week"],
                quarter_id=date_map["quarter"],
                day_of_the_week_id=date_map["day_of_the_week"],
                year_id=years[date_map["year"]],
                day_id=date_map["day"],
            )

        ins = dao.mega_ball_numbers.insert()
        dao.connection.execute(
            ins,
            number=hashmap["mega_ball"],
            month_id=date_map["month"],
            week_id=date_map["week"],
            quarter_id=date_map["quarter"],
            day_of_the_week_id=date_map["day_of_the_week"],
            year_id=years[date_map["year"]],
            day_id=date_map["day"],
        )


"""
Currently scrapes two days worth of data due to a lack of actual infrastructure setup, aka the cron job runs only on Fridays.
"""


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

        ins = dao.winners.insert()
        dao.connection.execute(
            ins,
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

        date_map = parse_date(hashmap["date"])

        ins = dao.regular_numbers.insert()
        for number in numbers:
            dao.connection.execute(
                ins,
                number=number,
                month_id=date_map["month"],
                week_id=date_map["week"],
                quarter_id=date_map["quarter"],
                day_of_the_week_id=date_map["day_of_the_week"],
                year_id=years[date_map["year"]],
                day_id=date_map["day"],
            )

        ins = dao.mega_ball_numbers.insert()
        dao.connection.execute(
            ins,
            number=hashmap["mega_ball"],
            month_id=date_map["month"],
            week_id=date_map["week"],
            quarter_id=date_map["quarter"],
            day_of_the_week_id=date_map["day_of_the_week"],
            year_id=years[date_map["year"]],
            day_id=date_map["day"],
        )
        if counter >= 1:
            break
        counter += 1


"""
Take the string date on the mega millions website
Convert that into a day of the week, day, month, year, week, and quarter values
"""


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


"""
Take the mega millions str ticket format of 'num - num ... - num - num'
And convert it into an integer number list
"""


def parse_numbers(numbers: str) -> list:
    final_numbers = []
    for number in numbers.split("-"):
        final_numbers.append(int(number.strip()))
    return final_numbers


# TODO - create calculateDaysAgo function
# Pseudo code
# in constants or helper python file the initial array or object with the mega millions number and the days ago value starting at 1 should exist
# calculateDaysAgo(daysAgoPrev: obj, winners: list) -> obj:
# take the array or object passed as an argument
# loop through the object
# set the winning lottery numbers as a dayAgo of one
# increment the rest by 1


# TODO - create updateDaysAgo function
# Pseudo code
# updateDaysAgo(winners: list) -> obj:
# query the DaysAgo table,
# query would pull all the numbers. for each number, pull the latest value
# pulling the latest can either involve using an array selector of last
# or (order by row id descending, first one should be the latest)
# depending on how this column is implemented
# create an object using the number and latest daysAgo value
