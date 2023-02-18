#!/usr/bin/env python3
import cmd
import os
import models
from models.base_model import BaseModel
from models.user import User
from colorama import Fore

class FBNBCommand(cmd.Cmd):

    clas = {
            'BaseModel',
            'User'
            }
    
    prompt = '({}{}) '.format(Fore.GREEN + "FBNB", Fore.RESET)

    def do_help(self, arg):
        if arg:
            try:
                print(eval("self.do_{}.__doc__".format(arg)))
            except AttributeError:
                print('{}{}: command does not exist'.format(Fore.RED + "ERROR", Fore.RESET))
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
        splitted = str(input_str).split(delimeter)

        sliced = [None] * arg_num
        for i, word in enumerate(splitted):
            if i < arg_num:
                sliced[i] = word
        # returns splitted list        
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
                    val = str(val)[1:-1]
                    setattr(obj, attr, val)
                    models.storage.save() 
                
if __name__ == "__main__":
    FBNBCommand().cmdloop()
