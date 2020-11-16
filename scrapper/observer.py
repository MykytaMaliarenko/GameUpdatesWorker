from abc import ABC, abstractmethod

from scrapper.updateinfo import UpdateInfo


class IObserver(ABC):
    @abstractmethod
    def update(self, update_info: UpdateInfo):
        pass


class IObservable(ABC):
    @abstractmethod
    def register_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def unregister_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify_observers(self, update_info: UpdateInfo):
        pass
