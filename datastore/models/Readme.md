# Models for mega millions data
* mega_millions - stores data associated with the actual winning numbers
* mega_millions_generated - stores data associated with generated tickets we are playing (simulated or real)


# Archive models

```python
class PureRandomTicketAttempts(Base, db.Model):
    __tablename__ = "pure_random_attempts"

    id = Column(Integer, primary_key=True)
    draw_date = Column(String(128), nullable=False)
    first_number = Column(Integer)
    second_number = Column(Integer)
    third_number = Column(Integer)
    fourth_number = Column(Integer)
    fifth_number = Column(Integer)
    mega_ball = Column(Integer)
    numbers_that_matched = Column(String(128))
    amt_of_numbers_that_matched = Column(Integer)
    winnings = Column(Integer)
    jackpot = Column(String(128))


class WeightedTicketAttempts(Base, db.Model):
    __tablename__ = "weighted_ticket_attempts"

    id = Column(Integer, primary_key=True)
    draw_date = Column(String(128), nullable=False)
    first_number = Column(Integer)
    second_number = Column(Integer)
    third_number = Column(Integer)
    fourth_number = Column(Integer)
    fifth_number = Column(Integer)
    mega_ball = Column(Integer)
    numbers_that_matched = Column(String(128))
    amt_that_matched = Column(Integer)
    jackpot = Column(String(128))


class ConnectedNumberOccurrences(Base, db.Model):
    __tablename__ = "connected_number_occurrences"

    id = Column(Integer, primary_key=True)
    lottery_number = Column(Integer, nullable=False)
    Number1 = Column(Integer, default=0)
    Number2 = Column(Integer, default=0)
    Number3 = Column(Integer, default=0)
    Number4 = Column(Integer, default=0)
    Number5 = Column(Integer, default=0)
    Number6 = Column(Integer, default=0)
    Number7 = Column(Integer, default=0)
    Number8 = Column(Integer, default=0)
    Number9 = Column(Integer, default=0)
    Number10 = Column(Integer, default=0)
    Number11 = Column(Integer, default=0)
    Number12 = Column(Integer, default=0)
    Number13 = Column(Integer, default=0)
    Number14 = Column(Integer, default=0)
    Number15 = Column(Integer, default=0)
    Number16 = Column(Integer, default=0)
    Number17 = Column(Integer, default=0)
    Number18 = Column(Integer, default=0)
    Number19 = Column(Integer, default=0)
    Number20 = Column(Integer, default=0)
    Number21 = Column(Integer, default=0)
    Number22 = Column(Integer, default=0)
    Number23 = Column(Integer, default=0)
    Number24 = Column(Integer, default=0)
    Number25 = Column(Integer, default=0)
    Number26 = Column(Integer, default=0)
    Number27 = Column(Integer, default=0)
    Number28 = Column(Integer, default=0)
    Number29 = Column(Integer, default=0)
    Number30 = Column(Integer, default=0)
    Number31 = Column(Integer, default=0)
    Number32 = Column(Integer, default=0)
    Number33 = Column(Integer, default=0)
    Number34 = Column(Integer, default=0)
    Number35 = Column(Integer, default=0)
    Number36 = Column(Integer, default=0)
    Number37 = Column(Integer, default=0)
    Number38 = Column(Integer, default=0)
    Number39 = Column(Integer, default=0)
    Number40 = Column(Integer, default=0)
    Number41 = Column(Integer, default=0)
    Number42 = Column(Integer, default=0)
    Number43 = Column(Integer, default=0)
    Number44 = Column(Integer, default=0)
    Number45 = Column(Integer, default=0)
    Number46 = Column(Integer, default=0)
    Number47 = Column(Integer, default=0)
    Number48 = Column(Integer, default=0)
    Number49 = Column(Integer, default=0)
    Number50 = Column(Integer, default=0)
    Number51 = Column(Integer, default=0)
    Number52 = Column(Integer, default=0)
    Number53 = Column(Integer, default=0)
    Number54 = Column(Integer, default=0)
    Number55 = Column(Integer, default=0)
    Number56 = Column(Integer, default=0)
    Number57 = Column(Integer, default=0)
    Number58 = Column(Integer, default=0)
    Number59 = Column(Integer, default=0)
    Number60 = Column(Integer, default=0)
    Number61 = Column(Integer, default=0)
    Number62 = Column(Integer, default=0)
    Number63 = Column(Integer, default=0)
    Number64 = Column(Integer, default=0)
    Number65 = Column(Integer, default=0)
    Number66 = Column(Integer, default=0)
    Number67 = Column(Integer, default=0)
    Number68 = Column(Integer, default=0)
    Number69 = Column(Integer, default=0)
    Number70 = Column(Integer, default=0)
```