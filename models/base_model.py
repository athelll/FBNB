#!/usr/bin/env python3
"""This is the basemodel class"""

from datetime import datetime
import models
import uuid

class BaseModel:
    """BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """initialization class"""

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    pass
                elif key in ("created_at", "updated_at"):
                    self.__dict__[key] = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """handles string representation of class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """saves change to basemodel"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """converst instance data into dictionary"""
        diction = self.__dict__.copy()
        diction['created_at'] = diction['created_at'].isoformat()
        diction['updated_at'] = diction['updated_at'].isoformat()
        diction['__class__'] = self.__class__.__name__
        return diction
