from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey

from .base import Base


class User(Base):
    __tablename__ = 'users_myuser'

    id = Column(Integer, primary_key=True)
    email = Column(Text)
    is_active = Column(Boolean)

    #notification_settings_id = Column(Integer, ForeignKey('notifications_notificationsettings.id'))
