from db.models import User
from scrapper.observer import AbstractObserver
from scrapper.updateinfo import UpdateInfo


class FirebasePopupNotifications(AbstractObserver):
    __firebase_server_key: str

    def update(self, update_info: UpdateInfo):
        pass

    @staticmethod
    def notify_user(user: User, update_info: UpdateInfo):
        pass
