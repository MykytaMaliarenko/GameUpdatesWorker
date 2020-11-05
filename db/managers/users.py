from typing import List

from db.models import Game, User


class UserManager:

    @staticmethod
    def get_subscribes(game: Game) -> List[User]:
        pass

    @staticmethod
    def get_firebase_tokens(user: User) -> List[str]:
        pass
