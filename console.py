#!/usr/bin/python3
"""
console module
"""
import cmd
import os
import shlex
from models.engine.file_storage import FileStorage
from models.user import User
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone"""

    prompt = "(hbnb) "

    def __init__(self):
        """initializes"""
        super().__init__()
        self.__storage = FileStorage()
        self.__classes = self.__storage.get_classes()

    def do_create(self, arg):
        """Create a new instance of BaseModel"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return

        # elif args not in self.__classes:
        #    print("** class doesn't exist **")

        # else:
        #    # print("why??????")
        #    # print(type(arg))
        #    instance = eval(arg)()
        #    instance.save()
        #    print(instance.id)
        """
        if len(args) == 1:
            print(type(arg[1]))
            return
        """

        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        obj = self.__classes[class_name]()
        """
        obj = eval(args)()

        print(type(obj))
        """
        # ===============
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Show the string representation of an instance"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in self.__storage.all():
            print("** no instance found **")
            return
        print(self.__storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in self.__storage.all():
            print("** no instance found **")
            return
        del self.__storage.all()[key]
        self.__storage.save()

    def do_all(self, arg):
        """Print all string representations of instances"""
        args = shlex.split(arg)
        if len(args) == 0:
            print([str(obj) for obj in self.__storage.all().values()])
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        print([obj for key, obj in self
               .__storage.all().items() if key.split('.')[0] == class_name])

        # print([str(obj) for key, obj in self
        #       .__storage.all().items() if key.split('.')[0] == class_name])

    def do_update(self, arg):
        """Update an instance based on the class name and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in self.__storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_name = args[2]
        attribute_value = args[3]
        obj = self.__storage.all()[key]
        setattr(obj, attribute_name, attribute_value)
        obj.save()

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def help_quit(self):
        """Help documentation for quit command"""
        print("Quit command: Quit the program")

    def do_EOF(self, arg):
        """Exit the program when EOF (Ctrl+D) is encountered"""
        print("")
        return True

    def help_EOF(self):
        """Help documentation for EOF command"""
        print("EOF command: Exit the program (Ctrl+D)")

    def do_clear(self):
        """Clear the console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def default(self, arg):
        """Allows the use of class name before argument"""
        args = arg.split('.')
        class_arg = args[0]
        if len(args) == 1:
            print("*** Unknown syntax: {}".format(arg))
            return
        try:
            args = args[1].split('(')
            command = args[0]
            if command == 'all':
                HBNBCommand.do_all(self, class_arg)
            elif command == 'count':
                HBNBCommand.do_count(self, class_arg)
            elif command == 'show':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_show(self, arg)
            elif command == 'destroy':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip('"')
                id_arg = id_arg.strip("'")
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_destroy(self, arg)
            elif command == 'update':
                args = args[1].split(',')
                id_arg = args[0].strip("'")
                id_arg = id_arg.strip('"')
                name_arg = args[1].strip(',')
                val_arg = args[2]
                name_arg = name_arg.strip(' ')
                name_arg = name_arg.strip("'")
                name_arg = name_arg.strip('"')
                val_arg = val_arg.strip(' ')
                val_arg = val_arg.strip(')')
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
            else:
                print("*** Unknown syntax: {}".format(arg))
        except IndexError:
            print("*** Unknown syntax: {}".format(arg))

    def do_count(self, line):
        """Display count of instances specified"""
        if line in self.__classes:
            count = 0
            for key, objs in self.__storage.all().items():
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()