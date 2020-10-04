from typing import List
from scrapper.updateinfo import UpdateInfo


class Scrapper:
    __observers: List

    def start(self):
        pass

    def __notify_observers(self, update_info: UpdateInfo):
        pass

    def register_observer(self, observer):
        pass

    def unregister_observer(self, observer):
        pass

    def __load_updates(self, game_id: int, limit: int) -> List[UpdateInfo]:
        pass
