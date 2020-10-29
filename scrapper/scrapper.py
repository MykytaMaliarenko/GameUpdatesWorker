import datetime
import time
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from typing import List, Dict
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

    @staticmethod
    async def __get_metadata(session, url: str, result: List[Dict[str, str]]):
        async with session.get(url) as response:
            raw = await response.text()
            soup = BeautifulSoup(raw, features="html.parser")
            result.append({
                'description': soup.find("meta", property="og:description")["content"],
                'image_url': soup.find("meta", property="og:image")["content"]
            })

    @staticmethod
    def __get_all_metadata(urls: List[str]):
        res = list()
        routines = list()

        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession(loop=loop)
        for url in urls:
            routines.append(loop.create_task(Scrapper.__get_metadata(session, url, res)))

        loop.run_until_complete(asyncio.wait(routines))
        loop.run_until_complete(asyncio.wait([session.close()]))
        loop.close()
        return res

    def __load_updates(self) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(self.game))
        if feed.status != 200 or len(feed.entries) == 0:
            raise Exception('rss feed doesn`t exist')

        entries_metedata = Scrapper.__get_all_metadata([entry.link for entry in feed.entries])

        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       game_id=self.game,
                       origin_url=entry.link,
                       short_description=entries_metedata[index]['description'],
                       image_url=entries_metedata[index]['image_url'])
            for index, entry in enumerate(feed.entries)
        ]
