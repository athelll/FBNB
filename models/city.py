#!/usr/bin/env python3
"""City Class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from models.place import Place
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """class"""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship('Place', cascade='all, delete, delete-orphan', backref="cities")
