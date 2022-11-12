## Project Overview

A combination of
- web scraper for pulling lottery win numbers - /scrape
- lottery ticket creator decision engine - /bizlogic
- datastore for cataloguing the winning numbers in a SQL type structure - /datastore/mega_millions_after_2013.db (will be generated after using make refresh in the setup instructions)
- datastore for cataloguing attempts from the creator engine - /datastore/
- scheduler - setup a cronjob to the scheduler/cron_mega_millions.sh this pulls the two latest winning numbers


## Setup Instructions

TODO. This will scrape winning numbers and generate the sqlite db:

```bash
# In a terminal
pip install -r requirements-dev.txt
make refresh
```

### TODOs

- Create tickets (Done)
- Save tickets to db (Done)
- Automate creating and saving the tickets on the day of the drawing (Tue, Fri) (Done)
- On the day after ticket is drawn, check the wins from the tickets created (Wed, Sat) and update (Done)
    - Send an email showing the ticket spread
- Save the total loss (Done)
- Add 
- Setup airflow / more robust scheduler than cronjob

### Commands to know

- python main.py run create_tickets 30
- python main.py run check_winnings random