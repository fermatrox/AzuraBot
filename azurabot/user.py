#!/usr/bin/env python3

"""
The User class for storing user data.
"""
from sqlalchemy.orm.exc import NoResultFound
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
    comment = Column(String(80))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now())

    def __init__(self, name):
        self.name = name
        self.comment = ""

    def __str__(self):
        return("User %s[%d]: \"%s\"" % (self.name, self.user_id,
                                        self.comment))


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

    # How to load many rows at once
    # =============================
    #
    # The "query" returned is an iterable containing all the
    # matching users.
    print("Loading non-existant user...")
    query = session.query(User).filter(User.name == "non-existant")
    for user in query:
        print(user)

    # How to load ONE row
    # ===================
    #
    # In this case, we don't get a "query" as a return value,
    # because we're using one(). That gives us ONE object in
    # return, of the correct type, so no need to iterate over
    # a query object.
    print("Loading one user which does exist...")
    try:
        user = session.query(User).filter(User.name == "Enfors").one()
        print(user)

    except NoResultFound:
        print("[that user doesn't exist]")

    # How to update and save
    # ======================
    user.comment = "www.OperationGYST.com"
    session.commit()

    print("Reloading user as user2...")
    try:
        user2 = session.query(User).filter(User.name == "Enfors").one()
        print(user2)

    except NoResultFound:
        print("[that user doesn't exist]")
