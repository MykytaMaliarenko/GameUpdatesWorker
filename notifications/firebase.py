import os
from typing import List
from scrapper.observer import UpdateObserver
from scrapper.updateinfo import UpdateInfo


class FirebasePopupNotifications(UpdateObserver):
    __FIREBASE_KEY = os.getenv("firebase_key")

    def on_new_update(self, update_info: UpdateInfo):
        pass

    def __get_all_users_by_subscription(self, game_id: int) -> List[str]:
        pass
