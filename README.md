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
- Automate creating and saving the tickets on the day of the drawing (Tue, Fri) (Done: Cron job currently running on raspberry pi)
- On the day after ticket is drawn, check the wins from the tickets created (Wed, Sat) and update (Done)
    - Send an email showing the ticket spread
    - Calculate and save the amount and the ticket numbers matched
- Save the total loss (Done)
- Add the winning ticket to the update email (Done)
- Figure out why a zero number can be created as part of the tickets (Done)
- Work in buying a megaplier ticket and doubling the none jackpot earnings for that spend
- Generate tickets that are weighted base on their occurrence
- Think about if I want just a purely random ticket generator
- Figure out doing power ball and mega ball tickets simultaneously
- Figure out the other lottery ticket games to see the odds
- Stretch goal, doing a weighted ticket using generated tickets to influence how new tickets are created
- Setup airflow / more robust scheduler than cronjob

### Commands to know

- python main.py run create_tickets 30
- python main.py run check_winnings random

### Articles for further exploration

- https://www.the-sun.com/money/6058825/lottery-algorithm-players-pick-best-scratchcards/
- https://www.the-sun.com/money/5921569/lottery-expert-reveals-million-dollar-winning-strategy/
- https://www.youtube.com/watch?v=Rjd6DODQ2XY&t=89s


### Powerball

- 1 - 69 regular numbers
- 1 - 26 power ball number
- Winning rules: https://powerball.com/games/home
- Past draws: 

### Mega Millions

- 1 - 70 regular numbers
- 1 - 25 mega ball number
- https://www.megamillions.com/How-to-Play.aspx#:~:text=Mega%20Millions%C2%AE%20tickets%20cost,winning%20numbers%20in%20a%20drawing.

### Other games to figure out

- New York Lotto
- Cash 4 Life
- Pick 10
- Take 5 Day
- Take 5 Eve
- Win 4 Day
- Numbers Day
- Numbers Eve