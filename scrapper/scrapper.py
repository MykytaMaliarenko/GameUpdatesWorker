import datetime
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from typing import List, Dict
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

    @staticmethod
    def load_updates(game_id: int) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(game_id))
        if feed.status != 200 or len(feed.entries) == 0:
            raise Exception('rss feed doesn`t exist')

        entries_metedata = Scrapper.__get_all_metadata([entry.link for entry in feed.entries])

        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       game_id=game_id,
                       origin_url=entry.link,
                       short_description=entries_metedata[index]['description'],
                       image_url=entries_metedata[index]['image_url'])
            for index, entry in enumerate(feed.entries)
        ]
