#!/usr/bin/env python3
"""This is the basemodel class"""

from datetime import datetime
import models
import uuid


class BaseModel:
    """BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """initialization class"""
        self.id = str(uuid.uuid4())
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    pass
                else:
                    self.__dict__[key] = value
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

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
        return diction
