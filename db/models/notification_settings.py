from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy import Column, Integer, TEXT, Table, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

association_table = Table('users_notificationsettings_notification_subscriptions', Base.metadata,
                          Column('notificationsettings_id', Integer, ForeignKey('notifications_notificationsettings.id')),
                          Column('game_id', Integer, ForeignKey('games_game.id')))


class NotificationSettings(Base):
    __tablename__ = 'notifications_notificationsettings'

    id = Column(Integer, primary_key=True)
    firebase_tokens = Column(ARRAY(TEXT))

    subscriptions = relationship("Game", secondary=association_table)

    def __repr__(self):
        return f"<NotificationSettings id={self.id}>"
