from db.models import User
from scrapper.updateinfo import UpdateInfo


class FirebasePopupNotifications:
    __firebase_server_key: str

    @staticmethod
    def notify_user(user: User, update_info: UpdateInfo):
        pass
