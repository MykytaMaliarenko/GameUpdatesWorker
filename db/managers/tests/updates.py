import unittest
import datetime

from db.managers.exceptions import GameNotFoundException
from db.instance import DBInstance
from db.managers.updates import UpdatesManager
from db.models import Game, GameBasedChannel, Update
from db.models.base import Base
from db.managers.tests import init_test_session

from scrapper.updateinfo import UpdateInfo


class TestUpdatesManager(unittest.TestCase):
    def setUp(self):
        self.session = init_test_session()

        self.game = Game(name='test game', steam_id=0)
        self.session.add(self.game)

        self.channel = GameBasedChannel(name='test channel')
        self.channel.game = self.game
        self.session.add(self.channel)

        self.session.commit()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(DBInstance.engine())

    def test_get_by_id(self):
        expected = Update(
            title='test title',
            description='test desc',
            publication_date=datetime.datetime.now(),
            origin_url='origin'
        )
        expected.game = self.game
        self.session.add(expected)
        self.session.commit()

        result = UpdatesManager.get_by_id(self.session, expected.id)
        self.assertEqual(expected, result)
        self.session.delete(result)

    def test_get_game_based_channel(self):
        expected = self.channel
        result = UpdatesManager.get_game_based_channel(self.session, self.game.steam_id)
        self.assertEqual(result, expected)

    def test_create_update(self):
        update_info = UpdateInfo(
            title='test title',
            description='test desc',
            publication_date=datetime.datetime.now(),
            origin_url='origin',
            steam_id=self.game.steam_id,
            image_url='',
            short_description='test short'
        )

        UpdatesManager.create_update(self.session, update_info)
        result = self.session.query(Update).filter(Update.title == update_info.title).one()
        assert result is not None
        self.assertEqual(result.title, update_info.title)
        self.session.delete(result)

    def test_get_last_update(self):
        update_info = UpdateInfo(
            title='test title',
            description='test desc',
            publication_date=datetime.datetime.now(),
            origin_url='origin',
            steam_id=self.game.steam_id,
            image_url='',
            short_description='test short'
        )
        UpdatesManager.create_update(self.session, update_info)

        update_info_2 = UpdateInfo(
            title='test title2',
            description='test desc2',
            publication_date=datetime.datetime.now() + datetime.timedelta(0, 3),
            origin_url='origin2',
            steam_id=self.game.steam_id,
            image_url='',
            short_description='test short2'
        )
        UpdatesManager.create_update(self.session, update_info_2)

        update = UpdatesManager.get_last_update(self.session, self.game.steam_id)
        self.assertEqual(update.title, "test title2")
        self.session.query(Update).delete()

    def test_get_last_update_not_exists(self):
        with self.assertRaises(GameNotFoundException):
            UpdatesManager.get_last_update(self.session, self.game.id)
