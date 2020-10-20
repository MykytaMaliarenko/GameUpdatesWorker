from typing import Any, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from .manager import AbstractFetchSingleEntity
from db.models import Update, GameBasedChannel

from scrapper.updateinfo import UpdateInfo


class UpdatesManager(AbstractFetchSingleEntity):
    @staticmethod
    def create_update(session: Session, update_info: UpdateInfo):
        channel = UpdatesManager.get_game_based_channel(session, update_info.game_id)

        update = Update.from_update_info(update_info)
        session.add(update)
        update.channel = channel

    @staticmethod
    def get_last_update(session: Session, game_id: int) -> Union[None, Update]:
        channel = UpdatesManager.get_game_based_channel(session, game_id)
        return session\
            .query(Update)\
            .filter(GameBasedChannel.id == channel.id)\
            .order_by(desc(Update.publication_date))\
            .first()

    @staticmethod
    def get_game_based_channel(session: Session, game_id: int) -> GameBasedChannel:
        channel = session. \
            query(GameBasedChannel). \
            filter(GameBasedChannel.game_id == game_id). \
            first()
        if channel is None:
            raise ValueError(f"game based channel for "
                             f"game with id={game_id} not found")

        return channel

    @staticmethod
    def _get_model() -> Any:
        return Update
