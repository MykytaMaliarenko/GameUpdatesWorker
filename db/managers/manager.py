from abc import ABC, abstractmethod
from typing import List, Any
from sqlalchemy.orm import Session


class IFetchMultipleEntities(ABC):
    @classmethod
    @abstractmethod
    def get_all(cls, session: Session) -> List[Any]:
        pass


class IFetchSingleEntities(ABC):
    @classmethod
    @abstractmethod
    def get_by_id(cls, session: Session, model_id: int) -> Any:
        pass


class IFetchable(ABC):
    @staticmethod
    @abstractmethod
    def _get_model() -> Any:
        pass


class AbstractFetchMultipleEntities(IFetchMultipleEntities, IFetchable):
    @classmethod
    def get_all(cls, session: Session) -> Any:
        return session.query(cls._get_model()).all()

    @staticmethod
    @abstractmethod
    def _get_model() -> Any:
        pass


class AbstractFetchSingleEntity(IFetchSingleEntities, IFetchable, ABC):
    @classmethod
    def get_by_id(cls, session: Session, model_id: int) -> List[Any]:
        return session.query(cls._get_model()).get(model_id)
