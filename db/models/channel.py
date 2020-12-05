from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class GameBasedChannel(Base):
    __tablename__ = 'channels_gamebasedchannel'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    game_id = Column(Integer, ForeignKey('games_game.id'))
    game = relationship("Game")

    subscriptions = relationship("Subscription")

    def __eq__(self, other):
        assert(isinstance(other, GameBasedChannel))
        return other.id == self.id
