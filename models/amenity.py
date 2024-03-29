#!/usr/bin/python3
"""
amenity model
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class that inherits from BaseModel
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes Amenity instance with name attribute
        """
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', "")
