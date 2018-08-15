#!/usr/bin/env python3

"""
The User class for storing user data.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now())

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return("User %s (%s)" % (self.name, self.user_id))


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    print("Creating user...")
    enfors = User("Enfors")
    session.add(enfors)
    session.commit()
    print(enfors)

    print("Loading user...")
    query = session.query(User).filter(User.name.like("Enfors"))
    for user in query:
        print(user)
