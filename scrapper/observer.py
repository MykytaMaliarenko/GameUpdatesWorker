from abc import abstractmethod

from db.managers.users import UserManager
from notifications.firebase import FirebasePopupNotifications
from scrapper import Scrapper


class UpdateObserver:

    @abstractmethod
    def update(self, scrapper: Scrapper) -> None:
        for user in UserManager.get_subscribes(scrapper.game):
            FirebasePopupNotifications.notify_user(user, scrapper.last_update)
