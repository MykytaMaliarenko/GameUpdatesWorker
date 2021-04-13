from typing import List, Generator

from pyfcm import FCMNotification
from loguru import logger

from db.models import User, GameBasedChannel
from db.managers.channels import GameBasedChannelsManager
from db.managers.users import UserManager
from db.instance import DBInstance
from scrapper.observer import IObserver
from scrapper.updateinfo import UpdateInfo


class FirebasePopupNotifications(IObserver):
    def __init__(self, firebase_server_key: str):
        self.service = FCMNotification(api_key=firebase_server_key)

    def update(self, update_info: UpdateInfo):
        session = DBInstance.get_instance().new_session()
        channel = GameBasedChannelsManager.get_game_based_channel(session, update_info.steam_id)
        subs = UserManager.get_subscribes(channel)
        session.close()
        self.__notify_users(channel, subs, update_info)

    def __notify_users(self, channel: GameBasedChannel, users: Generator[User], update_info: UpdateInfo):
        ids: List[str] = []
        for user in users:
            ids += user.firebase_tokens

        response = self.service.notify_multiple_devices(registration_ids=ids,
                                                        message_title=f"NEW UPDATE IN {channel.name}",
                                                        message_body=update_info.short_description)
        for message in response:
            if 'error' in message:
                logger.error(f"FCM ERROR {message}")
