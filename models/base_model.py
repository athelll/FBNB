#!/usr/bin/env python3
"""This is the basemodel class"""

import uuid
from datetime import datetime

class BaseModel:
    """BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """initialization class"""

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    pass
                elif key == "created_at":
                    self.created_at = datetime.strptime(kwargs[key],
                                                        "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(kwargs[key],
                                                       "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    setattr(self, key, value)
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """handles string representation of class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """saves change to basemodel"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """converst instance data into dictionary"""
        diction = self.__dict__
        diction['__class__'] = self.__class__.__name__
        diction['created_at'] = str(self.created_at.isoformat())
        diction['updated_at'] = str(self.updated_at.isoformat())
        return diction
