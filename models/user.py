#!/usr/bin/python
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            kwargs.pop('password', None)
            User.set_password_md5(self, pwd)
        super().__init__(*args, **kwargs)

    def set_password_md5(self, pwd):
        """ Method to set the pwd into MD5 algorithm """
        new_pwd = hashlib.md5()
        new_pwd.update(pwd.encode('utf-8'))
        encrypted_pwd = new_pwd.hexdigest()
        setattr(self, 'password', encrypted_pwd)
