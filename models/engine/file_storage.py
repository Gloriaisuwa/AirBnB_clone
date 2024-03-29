#!/usr/bin/python3
"""
FileStorage module
"""
import json
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage():
    """
    Serializes instances to a JSON file, deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}
    __classes = {"BaseModel": BaseModel, "User": User, "Place": Place,
                 "Amenity": Amenity, "City": City, "Review": Review,
                 "State": State}

    def __init__(self):
        """
        instantiates with a call to reload
        """
        self.reload()

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        Stores new object by <class name>.id in the __objects dictionary
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        """
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes JSON file to __objects
        """
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file:
                try:
                    data = json.load(file)
                    for key, value in data.items():
                        class_name, obj_id = key.split('.')
                        # cls = self.__classes.get(class_name)
                        cls = self.__classes[class_name]
                        self.__objects[key] = cls(**value)
                        """
                        else:
                            print(f"Warning: Class '{class_name}' not found.")
                        """

                except json.JSONDecodeError:
                    pass

    def get_classes(self):
        """
        Returns the dictionary of class names to classes
        """
        return self.__classes
