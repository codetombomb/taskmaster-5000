from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from prettycli import green, color
from .base import Base
from helpers import Prompt

prompt = Prompt()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String(30), unique=True)
    birthday = Column(DateTime)
    
    tasks = relationship("Task", backref=backref("the_user"))
    
    @classmethod
    def find_by(cls, session, **kwargs):
        found_user = session.query(cls).filter_by(**kwargs).first()
        if found_user:
            return found_user
        
    @classmethod
    def save_user(cls, session, **kwargs):
        new_user = cls(**kwargs)

        session.add(new_user)
        session.commit()
    
        return session.query(User).order_by(User.id.desc()).first()
    
    def __repr__(self):
        id = str(self.id)
        birthday = str(self.birthday)
        
        return \
            green(f"\n<User ") + \
            color(f"id={color(id).rgb_fg(132, 209, 50)}, ").rgb_fg(83, 36,224) + \
            color(f"first_name={color(self.first_name).rgb_fg(132, 209, 50)}, ").rgb_fg(83, 36,224) + \
            color(f"last_name={color(self.last_name).rgb_fg(132, 209, 50)}, ").rgb_fg(83, 36,224) + \
            color(f"username={color(self.username).rgb_fg(132, 209, 50)}, ").rgb_fg(83, 36,224) + \
            color(f"birthday={color(birthday).rgb_fg(132, 209, 50)}").rgb_fg(83, 36,224) + \
            green(">")
