from .exceptions import GameBasedChannelNotFoundException
from typing import Any, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from .manager import AbstractFetchSingleEntity
from db.managers.channels import GameBasedChannelsManager
from db.models import Update, GameBasedChannel

from scrapper.updateinfo import UpdateInfo


class UpdatesManager(AbstractFetchSingleEntity):
    @staticmethod
    def create_update(session: Session, update_info: UpdateInfo):
        channel = GameBasedChannelsManager.get_game_based_channel(session, update_info.steam_id)

        update = Update.from_update_info(update_info)
        session.add(update)
        update.channel = channel

    @staticmethod
    def get_last_update(session: Session, steam_id: int) -> Union[None, Update]:
        channel = GameBasedChannelsManager.get_game_based_channel(session, steam_id)
        return session\
            .query(Update)\
            .filter(Update.channel_id == channel.id)\
            .order_by(desc(Update.publication_date))\
            .first()

    @staticmethod
    def _get_model() -> Any:
        return Update
