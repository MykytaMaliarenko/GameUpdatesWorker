from typing import List

from db.models import Game, User


class UserManager:
    def get_subscribes(self, game: Game) -> List[User]:
        pass

    def get_firebase_tokens(self, user: User) -> List[str]:
        pass
