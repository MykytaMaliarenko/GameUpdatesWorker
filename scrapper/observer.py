from abc import abstractmethod

from scrapper.updateinfo import UpdateInfo


class UpdateObserver:

    @abstractmethod
    def update(self, update_info: UpdateInfo):
        pass
