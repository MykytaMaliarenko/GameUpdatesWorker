import time
import asyncio
import datetime
from typing import List, Dict

import aiohttp
import pytz
import feedparser
from bs4 import BeautifulSoup

from loguru import logger

from .exceptions import FeedDoesntExist
from db.instance import DBInstance
from db.managers.games import GamesManager
from db.managers.updates import UpdatesManager
import db.managers.exceptions as db_exceptions
from db.models import Game

from scrapper.observer import AbstractObserver
from scrapper.updateinfo import UpdateInfo


class Scrapper:

    def __init__(self):
        self.__observers: List[AbstractObserver] = []

    def start(self, sleep_time: int = 300):
        while True:
            general_session = DBInstance.get_instance().new_session()
            games: List[Game] = GamesManager.get_all(general_session)
            general_session.close()

            for game in games:
                session = DBInstance.get_instance().new_session()

                logger.info(f"start polling updates for {game.name}")
                if not UpdatesManager.has_game_based_channel(session, game.steam_id):
                    logger.warning(f"game based channel was not found {game.name}")
                    session.close()
                    logger.info(f"session closed")
                    continue

                try:
                    last_update_in_db = UpdatesManager.get_last_update(session, game.steam_id)

                    updates = self.__load_updates(game.steam_id)
                    for update in updates:
                        update_date = pytz.UTC.localize(update.publication_date)
                        last_update_date = last_update_in_db.publication_date

                        if update_date > last_update_date:
                            logger.info(f"new_update "
                                        f"title={update.title} "
                                        f"publication_date={last_update_in_db.publication_date}")

                            UpdatesManager.create_update(session, update)
                            logger.info(f"added to session")

                            self.__notify_observers(update)
                            logger.info(f"notified all observers")

                    session.commit()
                    logger.info(f"session committed")
                except (db_exceptions.GameBasedChannelNotFoundException, FeedDoesntExist) as err:
                    session.rollback()
                    logger.info(f"session rollback")
                    logger.exception(str(err))
                finally:
                    session.close()
                    logger.info(f"session closed")

            time.sleep(sleep_time)

    def __notify_observers(self, update_info: UpdateInfo) -> None:
        for observer in self.__observers:
            observer.update(update_info)

    def register_observer(self, observer: AbstractObserver) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def unregister_observer(self, observer: AbstractObserver) -> None:
        self.__observers.remove(observer)

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
            routines.append(Scrapper.__get_metadata(session, url, res))

        loop.run_until_complete(asyncio.wait(routines))
        loop.run_until_complete(asyncio.wait([session.close()]))
        return res

    @staticmethod
    def __load_updates(steam_id: int) -> List[UpdateInfo]:
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(steam_id))
        if feed.status != 200 or len(feed.entries) == 0:
            raise FeedDoesntExist(steam_id)

        links = [entry.link for entry in feed.entries]
        entries_metedata = Scrapper.__get_all_metadata(links)

        return [
            UpdateInfo(title=entry.title,
                       description=entry.summary,
                       publication_date=datetime.datetime(*(entry.published_parsed[0:6])),
                       steam_id=steam_id,
                       origin_url=entry.link,
                       short_description=entries_metedata[index]['description'],
                       image_url=entries_metedata[index]['image_url'])
            for index, entry in enumerate(feed.entries)
        ]
