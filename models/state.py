#!/usr/bin/env python3
"""State Class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from models.city import City
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """Class"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='all, delete, delete-orphan', backref="state")

    @property
    def cities(self):
        store = models.storage.all(City)
        result = []
        for city in store.values():
            if city.state_id == self.id:
                result.append(city)
        return result

