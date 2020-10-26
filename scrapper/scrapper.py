import datetime
from typing import List
import feedparser

from scrapper.updateinfo import UpdateInfo


class Scrapper:

    def __init__(self, game_id):
        self.game_id = game_id
        self.__observers: List = []

    def notify_observers(self, update_info: UpdateInfo):
        for observer in self.__observers:
            observer.update(update_info)

    def register_observer(self, observer):
        self.__observers.append(observer)

    def unregister_observer(self, observer):
        self.__observers.remove(observer)

    def __load_updates(self) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(self.game_id))
        if feed.status != 200 or len(feed.entries) == 0:
            raise Exception('rss feed doesn`t exist')
        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       game_id=self.game_id)
            for entry in feed.entries
        ]
