from db.models import User
from scrapper.updateinfo import UpdateInfo


class FirebasePopupNotifications:
    __firebase_key: str

    def __notify_user(self, user: User, update_info: UpdateInfo):
        pass
