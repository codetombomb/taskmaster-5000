from datetime import datetime
from .base import Base
from helpers.prompt import Prompt
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from prettycli import blue, green, color, red

prompt = Prompt()

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    description = Column(String(150), nullable=False)
    complete = Column(Boolean, default=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("user.id"))

    @classmethod
    def get_description(cls):
        description = prompt.ask("Please enter a short description of the task: ")
        return description

    @classmethod
    def get_year(cls):
        year = prompt.ask("Please enter the year in which this is due (ex. 20XX): ")
        if year.isdigit():
            if datetime.now().year <= int(year) <= datetime.now().year + 5:
                return year
            else:
                print(red("That was invalid."))
                return cls.get_year()
        else:
            print(red("That was invalid."))
            return cls.get_year()

    @classmethod
    def get_month(cls):
        month = prompt.ask("Please enter the month in which this is due 1-12: ")
        if month.isdigit():
            if 1 <= int(month) <= 12:
                return month
            else:
                print(red("That was invalid."))
                return cls.get_month()
        else:
            print(red("That was invalid."))
            return cls.get_month()

    @classmethod
    def get_day(cls):
        day = prompt.ask("Please enter the day in which this is due 1-31: ")
        if day.isdigit():
            if 0 >= int(day) >= 31:
                print(red("That was invalid."))
                return cls.get_day()
            else:
                return day
        else:
            print(red("That was invalid."))
            return cls.get_day()

    @classmethod
    def create_date_string(cls, y, m, d):
        try:
            datetime(int(y), int(m), int(d))
            return f"{y}-{m}-{d}"
        except ValueError:
            return False

    def mark_complete(self, session):
        self.complete = True
        session.add(self)
        session.commit()
        return self

    def update(self, session, new_description):
        self.description = new_description
        session.add(self)
        session.commit()
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
        return self

    def __repr__(self):
        id = str(self.id)
        complete = str(self.complete)
        due_date = str(self.due_date)
        created_at = str(self.created_at)

        return (
            green(f"\n<Task ")
            + color(f"id={color(id).rgb_fg(132, 209, 50)}, ").rgb_fg(83, 36, 224)
            + color(
                f"description={color(self.description).rgb_fg(132, 209, 50)}, "
            ).rgb_fg(83, 36, 224)
            + color(f"complete={color(complete).rgb_fg(132, 209, 50)}, ").rgb_fg(
                83, 36, 224
            )
            + color(f"due_date={color(due_date).rgb_fg(132, 209, 50)}, ").rgb_fg(
                83, 36, 224
            )
            + color(f"created_at={color(created_at).rgb_fg(132, 209, 50)}, ").rgb_fg(
                83, 36, 224
            )
            + green(">")
        )
