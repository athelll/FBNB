#!/usr/bin/env python3
"""User Class"""

from models.base_model import BaseModel


class User(BaseModel):
    """Class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
