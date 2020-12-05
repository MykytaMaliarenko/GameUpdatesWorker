from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users_myuser'

    id = Column(Integer, primary_key=True)
    email = Column(Text)
    is_active = Column(Boolean)


class Subscription(Base):
    __tablename__ = 'users_subscription'

    notify = Column(Boolean, default=False)

    game_based_channel_id = Column(Integer,
                                   ForeignKey('channels_gamebasedchannel.id'),
                                   nullable=True)
    game_based_channel = relationship("GameBasedChannel", nullable=True)

    user_id = Column(Integer, ForeignKey('users_myuser.id'))
    user = relationship("User", back_populates="subscriptions")
