#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

model = [User, State, City, Amenity, Place, Review]

class DBStorage:
    """create tables in environment"""
    __engine = None
    __session = None

    def __init__(self):
        """initiralizes the db_storage instance"""

        ENV = getenv('HBNB_ENV') # running environment
        USER = getenv('HBNB_MYSQL_USER') # Mysql username
        PWD = "hbnb_dev_pwd"# getenv('HBNB_MYSQL_PWD') # Mysql password
        HOST = getenv('HBNB_MYSQL_HOST') # Mysql hostname
        DB = getenv('HBNB_MYSQL_DB') # Database name

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(USER, PWD, HOST, DB),
                                      pool_pre_ping=True)
        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        result_temp = []
        result = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            result_temp = self.__session.query(cls).all()
        else:
            for clas in model:
                queries = self.__session.query(clas).all()
                for obj in queries:
                    result_temp.append(obj)

        for obj in result_temp:
            result["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

        return result

    def new(self, obj):
        """add new object to db"""
        self.__session.add(obj)

    def save(self):
        """commit to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes for the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads from db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
