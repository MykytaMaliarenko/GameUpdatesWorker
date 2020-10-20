from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base
from .notification_settings import association_table


class Game(Base):
    __tablename__ = 'games_game'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    steam_id = Column(Integer)

    subscribers = relationship(
        "NotificationSettings",
        secondary=association_table
    )

    def steam_rss(self) -> str:
        pass

    def __repr__(self):
        return f"<Game id={self.id} name={self.name} steam_id={self.steam_id}>"
