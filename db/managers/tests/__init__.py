import main

from sqlalchemy.orm import Session
from db.models.base import Base

from db.instance import DBInstance


def init_test_session() -> Session:
    main.init_local_env(f"../../../{main.LOCAL_ENV}")
    session: Session = DBInstance.get_instance(is_test=True).new_session()
    Base.metadata.create_all(DBInstance.engine())
    return session
