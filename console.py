#!/usr/bin/env python3
"""This is the console"""


import cmd
import os
import models
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from colorama import Fore


class FBNBCommand(cmd.Cmd):
    """Console"""

    clas = {
            'BaseModel',
            'User',
            'State',
            'City',
            'Amenity',
            'Place',
            'Review'
            }

    prompt = '({}{}) '.format(Fore.GREEN + "FBNB", Fore.RESET)

    def do_help(self, arg):
        """I tell you what commands do"""
        if arg:
            try:
                print(eval("self.do_{}.__doc__".format(arg)))
            except AttributeError:
                print('({}{}) command does not exist'.format(
                    Fore.RED + "ERROR", Fore.RESET))
                return
        else:
            return super().do_help(arg)

    def do_EOF(self, line):
        """exits console"""
        return True

    def emptyline(self):
        pass

    def do_quit(self, line):
        """quits or exits console"""
        return True

    def do_clear(self, line):
        """clears screen"""
        os.system('clear')

    def do_create(self, line):
        """creates a new class"""
        if line == "":
            print('** class name missing **')
            return

        if line in self.clas:
            cls = eval("{}()".format(line))
            print(cls.id)
            models.storage.new(cls)
            models.storage.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """shows class object with argumented id"""
        if line == "":
            print('** class name missing **')
            return

        try:
            cls, idd = str(line).split()
        except ValueError:
            cls, idd = line, ""

        if cls in self.clas:
            if idd != "":
                objs = models.storage.all()
                for obj in objs.values():
                    if obj.__class__.__name__ == cls:
                        if idd == obj.id:
                            print(obj)
                            return
                print("** no instance found **")
            else:
                print('** instance id missing **')
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """destroys an object and updates storage engine"""
        if line == "":
            print('** class name missing **')
            return

        try:
            cls, idd = str(line).split()
        except ValueError:
            cls, idd = line, ""

        if cls in self.clas:
            if idd != "":
                objs = models.storage.all()
                for key, obj in objs.items():
                    if obj.__class__.__name__ == cls:
                        if idd == obj.id:
                            del objs[key]
                            models.storage.save()
                            return
                print('** no instance found **')
            else:
                print('** instance id missing **')
        else:
            print("** class doesn't exist **")

    def do_all(self, line):
        """prints all created objects"""
        objs = models.storage.all()
        if line == "":
            for obj in objs.values():
                print(obj)
        elif line in self.clas:
            for obj in objs.values():
                if obj.__class__.__name__ == line:
                    print(obj)
        else:
            print("** class doesn't exist **")

    @staticmethod
    def my_split(input_str, delimeter, arg_num):
        """splits the arguments"""
        splitted = str(input_str).split(delimeter)

        sliced = [None] * arg_num
        for i, word in enumerate(splitted):
            if i < arg_num:
                sliced[i] = word

        return sliced

    def do_update(self, line):
        """updates an objects data"""

        if line == "":
            print('** class name missing **')
            return

        cls, idd, attr, val = FBNBCommand.my_split(line, " ", 4)
        objects = models.storage.all().values()
        ids = [i.id for i in objects]

        if cls not in self.clas:
            print("** class doesn't exist **")
        elif idd is None:
            print("** instance id missing **")
        elif idd not in ids:
            print("** no instance found **")
        elif attr is None:
            print("** attribute name missing **")
        elif val is None:
            print("** value missing **")
        else:
            for obj in objects:
                if idd == obj.id:
                    if val[0] == "\"" and val[-1] == "\"":
                        val.replace("\"", "")
                    setattr(obj, attr, val)
                    models.storage.save()

    def do_count(self, line):
        objs = models.storage.all()
        if line in self.clas:
            counter = 0
            for obj in objs.values():
                if obj.__class__.__name__ == line:
                    counter += 1
            print(counter)
        else:
            print("** no instance found **")

    def default(self, line: str):

        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]

        commands = {"all": self.do_all,
                    "count": self.do_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
                or args[1] not in commands.keys():
            super().default(line)
            return

        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            params = re.match(r"\"(.+?)\", (.+)", args[2])
            if params.groups()[1][0] == '{':
                dic_p = eval(params.groups()[1])
                for k, v in dic_p.items():
                    commands[args[1]](args[0] + " " + params.groups()[0] +
                                      " " + k + " " + str(v))
            else:
                rest = params.groups()[1].split(", ")
                commands[args[1]](args[0] + " " + params.groups()[0] + " " +
                                  rest[0] + " " + rest[1])


if __name__ == "__main__":
    FBNBCommand().cmdloop()
