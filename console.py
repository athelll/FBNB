#!/usr/bin/env python3
import cmd
import os
import models
from models.base_model import BaseModel
from colorama import Fore

class FBNBCommand(cmd.Cmd):

    clas = {
            'BaseModel'
            }
    
    prompt = '({}{}) '.format(Fore.BLUE + "FBNB", Fore.RESET)

    def do_help(self, arg):
        if arg:
            try:
                print(eval("self.do_{}.__doc__".format(arg)))
            except AttributeError:
                print('ERROR: command does not exist')
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
        if line in self.clas or line == "":
            objs = models.storage.all()
            for obj in objs.values():
                print(obj)

        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """updates an objects data"""
        pass
        

        
        
if __name__ == "__main__":
    FBNBCommand().cmdloop()
