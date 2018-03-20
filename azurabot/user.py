#!/usr/bin/env python3

"""
The User class for storing user data.
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime


class User:
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now())

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return("User %d (%d)" % (self.name, self.user_id))
