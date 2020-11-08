from typing import Any

from .exceptions import GameNotFoundException
from .manager import AbstractFetchMultipleEntities
from db.models import Game


class GamesManager(AbstractFetchMultipleEntities):

    @staticmethod
    def get_game_by_steam_id(session, steam_id: int):
        game = session. \
            query(Game). \
            filter(Game.steam_id == steam_id). \
            first()
        if game is None:
            raise GameNotFoundException()

        return game

    @staticmethod
    def _get_model() -> Any:
        return Game
