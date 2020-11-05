from typing import Any

from .manager import AbstractFetchMultipleEntities
from db.models import Game


class GamesManager(AbstractFetchMultipleEntities):

    @staticmethod
    def _get_model() -> Any:
        return Game
