import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBInstance(metaclass=MetaSingleton):
    __engine = None
    __Session = None

    def __init__(self, is_test: bool = False):
        DBInstance.__engine = create_engine(os.getenv(
            "db_connection_str" if not is_test else "test_db_connection_str"
        ))
        DBInstance.__Session = sessionmaker(bind=DBInstance.__engine)

    @staticmethod
    def with_session(func):
        def wrapper(*args, **kwargs):
            session = DBInstance.get_instance().new_session()

            new_args = args
            if len(args) != 0:
                new_args = list()
                new_args.append(session)
                new_args.extend(args)
                new_args = tuple(new_args)
            else:
                kwargs['session'] = session

            result = func(*new_args, **kwargs)
            session.close()
            return result

        return wrapper

    def new_session(self) -> Session:
        return self.__Session()

    @staticmethod
    def engine():
        return DBInstance.__engine

    @classmethod
    def get_instance(cls, **kwargs):
        return DBInstance(**kwargs)
