from abc import ABC, abstractmethod

from scrapper.updateinfo import UpdateInfo


class AbstractObserver(ABC):
    __COUNTER = 0

    def __init__(self):
        self.__id = AbstractObserver.__COUNTER
        AbstractObserver.__COUNTER += 1

    @abstractmethod
    def update(self, update_info: UpdateInfo):
        pass

    def __eq__(self, other):
        assert isinstance(other, AbstractObserver)
        return self.__id == other.__id
