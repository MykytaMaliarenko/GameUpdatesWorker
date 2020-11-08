from .exceptions import GameBasedChannelNotFoundException
from typing import Any, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from .manager import AbstractFetchSingleEntity
from db.managers.games import GamesManager
from db.models import Update, GameBasedChannel

from scrapper.updateinfo import UpdateInfo


class UpdatesManager(AbstractFetchSingleEntity):
    @staticmethod
    def create_update(session: Session, update_info: UpdateInfo):
        channel = UpdatesManager.get_game_based_channel(session, update_info.steam_id)

        update = Update.from_update_info(update_info)
        session.add(update)
        update.channel = channel

    @staticmethod
    def get_last_update(session: Session, steam_id: int) -> Union[None, Update]:
        channel = UpdatesManager.get_game_based_channel(session, steam_id)
        return session\
            .query(Update)\
            .filter(GameBasedChannel.id == channel.id)\
            .order_by(desc(Update.publication_date))\
            .first()

    @staticmethod
    def has_game_based_channel(session: Session, steam_id: int) -> bool:
        try:
            UpdatesManager.get_game_based_channel(session, steam_id)
            return True
        except GameBasedChannelNotFoundException:
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
        return Update
