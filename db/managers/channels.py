from typing import Any

from sqlalchemy.orm import Session

from .exceptions import GameBasedChannelNotFoundException, GameNotFoundException

from db.models import GameBasedChannel
from .games import GamesManager
from .manager import AbstractFetchSingleEntity


class GameBasedChannelsManager(AbstractFetchSingleEntity):

    @staticmethod
    def has_game_based_channel(session: Session, steam_id: int) -> bool:
        try:
            game = GamesManager.get_game_by_steam_id(session, steam_id)
            return session\
                .query(session.query(GameBasedChannel).filter(GameBasedChannel.game_id == game.id).exists())\
                .scalar()
        except GameNotFoundException:
            return False

    @staticmethod
    def get_game_based_channel(
            session: Session,
            steam_id: int) -> GameBasedChannel:

        game = GamesManager.get_game_by_steam_id(session, steam_id)

        channel = session. \
            query(GameBasedChannel). \
            filter(GameBasedChannel.game_id == game.id). \
            first()
        if channel is None:
            raise GameBasedChannelNotFoundException()

        return channel

    @staticmethod
    def _get_model() -> Any:
        return GameBasedChannel
