import datetime
from typing import List
import feedparser

from scrapper.updateinfo import UpdateInfo


class Scrapper:
    __observers: List

    def start(self):
        pass

    def __notify_observers(self, update_info: UpdateInfo):
        pass

    def register_observer(self, observer):
        pass

    def unregister_observer(self, observer):
        pass

    @staticmethod
    def __load_updates(game_id: int) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(game_id))
        if feed.status != 200 or len(feed.entries) == 0:
            raise Exception('rss feed doesn`t exist')

        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       game_id=game_id)
            for entry in feed.entries
        ]
