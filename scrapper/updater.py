from typing import List
import feedparser

from scrapper.updateinfo import UpdateInfo


class Updater:
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
    def load_updates(game_id: int) -> List[UpdateInfo]:
        list_of_updates = []
        feed = feedparser.parse("https://store.steampowered.com/feeds/newshub/app/" + str(game_id))
        for elem in feed.feed.links:
            if 'https://store.steampowered.com/newshub/app/' + str(game_id) + '/' not in elem.values():
                raise Exception('rss feed doesn`t exist')
        for entry in feed.entries:
            update_title = entry.title
            update_published_at = entry.published
            update_description = entry.summary
            list_of_updates.append(UpdateInfo(update_title, update_description, update_published_at, game_id))
        return list_of_updates
