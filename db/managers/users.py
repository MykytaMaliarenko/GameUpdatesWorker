from typing import Generator

from db.models import User, GameBasedChannel


class UserManager:

    @staticmethod
    def get_subscribes(channel: GameBasedChannel) -> Generator[User]:
        return (subscription.user for subscription in channel.subscriptions)
