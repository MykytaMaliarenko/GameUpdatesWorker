from scrapper.updateinfo import UpdateInfo
from abc import abstractmethod


class UpdateObserver:
    @abstractmethod
    def on_new_update(self, update_info: UpdateInfo):
        pass
