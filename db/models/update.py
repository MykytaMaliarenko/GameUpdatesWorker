from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from scrapper.updateinfo import UpdateInfo
from .base import Base


class Update(Base):
    __tablename__ = 'channels_update'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    views = Column(Integer)
    publication_date = Column(DateTime(timezone=True))

    origin_url = Column(String)

    channel_id = Column(Integer, ForeignKey('channels_gamebasedchannel.id'))
    channel = relationship("GameBasedChannel")

    @staticmethod
    def from_update_info(update_info: UpdateInfo):
        instance = Update(
            title=update_info.title,
            description=update_info.description,
            views=0,
            origin_url=update_info.origin_url
        )
        instance.publication_date = update_info.publication_date
        return instance

    def __eq__(self, other):
        assert(isinstance(other, Update))
        return self.id == other.id

    def __repr__(self):
        return f"<Update id={self.id} title={self.title}>"
