#!/usr/bin/env python3
"""This is the basemodel class"""

import models
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String , Integer, DateTime

Base = declarative_base()

class BaseModel:
    """BaseModel Class"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default = datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default = datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """initialization class"""
        self.id = str(uuid.uuid4())
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """handles string representation of class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """saves change to basemodel"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """converst instance data into dictionary"""
        diction = self.__dict__.copy()
        diction['created_at'] = self.created_at.isoformat()
        diction['updated_at'] = self.updated_at.isoformat()
        diction['__class__'] = self.__class__.__name__
        try:
            del diction['_sa_instance_state']
        except KeyError:
            pass
        return diction

    def delete(self):
        models.storage.delete(obj=self)
