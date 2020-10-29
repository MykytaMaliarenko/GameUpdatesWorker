import datetime
import time
from typing import List
import feedparser

from db.models import Game
from scrapper.observer import UpdateObserver
from scrapper.updateinfo import UpdateInfo


class Scrapper:

    def __init__(self, game: Game):
        self.game = game
        self.__observers: List[UpdateObserver] = []
        self.last_update = self.__load_updates()[-1]

    def __notify_observers(self, scrapper) -> None:
        for observer in self.__observers:
            observer.update(scrapper)

    def register_observer(self, observer: UpdateObserver) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)
        else:
            print(f'Failed to add: {observer}')

    def unregister_observer(self, observer: UpdateObserver) -> None:
        try:
            self.__observers.remove(observer)
        except ValueError:
            print(f'Failed to remove: {observer}')

    def __if_game_has_new_update(self) -> None:
        __current_update = self.__load_updates()[-1]
        if self.last_update == __current_update:
            self.last_update = __current_update
            self.__notify_observers(self)

    def permanent_update_check(self):
        while True:
            self.__if_game_has_new_update()
            time.sleep(60)

    def __load_updates(self) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(self.game.id))
        if feed.status != 200 or len(feed.entries) == 0:
            raise Exception('rss feed doesn`t exist')
        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       game_id=self.game.id,
                       origin_url='')
            for entry in feed.entries
        ]
