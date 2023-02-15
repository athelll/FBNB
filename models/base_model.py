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
        diction = {}
        for keys, values in self.__dict__.items():
            if keys == 'created_at' or keys == 'updated_at':
                diction[keys] = values.isoformat()
            else:
                diction[keys] = values     
        diction['__class__'] = self.__class__.__name__

        return diction
