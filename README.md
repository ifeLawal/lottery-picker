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

- Setup airflow / more robust scheduler than cronjob