from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from datastore.models import Base, db


class Winners(Base, db.Model):
    __tablename__ = "winners"

    id = Column(Integer, primary_key=True)
    draw_date = Column(String(128), nullable=False)
    first_number = Column(Integer)
    second_number = Column(Integer)
    third_number = Column(Integer)
    fourth_number = Column(Integer)
    fifth_number = Column(Integer)
    mega_ball = Column(Integer)
    megaplier = Column(Integer)
    jackpot = Column(String(128))

    def __repr__(self):
        return f"Winners(id={self.id!r}, draw_date={self.draw_date!r}, numbers={self.first_number!r}-{self.second_number!r}-{self.third_number!r}-{self.fourth_number!r}-{self.fifth_number!r}, mega_ball={self.mega_ball!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RegularNumbers(Base, db.Model):
    __tablename__ = "regular_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    month_id = Column(Integer, ForeignKey("months.id"), nullable=False)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    day_of_the_week_id = Column(
        Integer, ForeignKey("days_of_the_week.id"), nullable=False
    )
    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)

    months = relationship("Months", back_populates="regular_numbers")
    weeks = relationship("Weeks", back_populates="regular_numbers")
    quarters = relationship("Quarters", back_populates="regular_numbers")
    days_of_the_week = relationship("DaysOfTheWeek", back_populates="regular_numbers")
    years = relationship("Years", back_populates="regular_numbers")
    days = relationship("Days", back_populates="regular_numbers")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.number!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MegaBallNumbers(Base, db.Model):
    __tablename__ = "mega_ball_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    month_id = Column(Integer, ForeignKey("months.id"), nullable=False)
    week_id = Column(Integer, ForeignKey("weeks.id"), nullable=False)
    quarter_id = Column(Integer, ForeignKey("quarters.id"), nullable=False)
    day_of_the_week_id = Column(
        Integer, ForeignKey("days_of_the_week.id"), nullable=False
    )
    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)

    months = relationship("Months", back_populates="mega_ball_numbers")
    weeks = relationship("Weeks", back_populates="mega_ball_numbers")
    quarters = relationship("Quarters", back_populates="mega_ball_numbers")
    days_of_the_week = relationship("DaysOfTheWeek", back_populates="mega_ball_numbers")
    years = relationship("Years", back_populates="mega_ball_numbers")
    days = relationship("Days", back_populates="mega_ball_numbers")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.number!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Months(Base, db.Model):
    __tablename__ = "months"

    id = Column(Integer, primary_key=True)
    month = Column(String(128), nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="months")
    mega_ball_numbers = relationship("MegaBallNumbers", back_populates="months")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.month!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DaysOfTheWeek(Base, db.Model):
    __tablename__ = "days_of_the_week"

    id = Column(Integer, primary_key=True)
    day_of_the_week = Column(String(128), nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="days_of_the_week")
    mega_ball_numbers = relationship(
        "MegaBallNumbers", back_populates="days_of_the_week"
    )

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.day_of_the_week!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Weeks(Base, db.Model):
    __tablename__ = "weeks"

    id = Column(Integer, primary_key=True)
    week = Column(Integer, nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="weeks")
    mega_ball_numbers = relationship("MegaBallNumbers", back_populates="weeks")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.week!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Quarters(Base, db.Model):
    __tablename__ = "quarters"

    id = Column(Integer, primary_key=True)
    quarter = Column(String(128), nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="quarters")
    mega_ball_numbers = relationship("MegaBallNumbers", back_populates="quarters")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.quarter!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Years(Base, db.Model):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="years")
    mega_ball_numbers = relationship("MegaBallNumbers", back_populates="years")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.year!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Days(Base, db.Model):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True)
    day = Column(Integer, nullable=False)

    regular_numbers = relationship("RegularNumbers", back_populates="days")
    mega_ball_numbers = relationship("MegaBallNumbers", back_populates="days")

    def __repr__(self):
        return f"Number(id={self.id!r}, number={self.day!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
