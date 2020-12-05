import unittest
import datetime

from db.instance import DBInstance
from db.managers.channels import GameBasedChannelsManager
from db.models import Game, GameBasedChannel, Update
from db.models.base import Base
from db.managers.tests import init_test_session


class TestGameBasedChannelsManager(unittest.TestCase):
    # noinspection DuplicatedCode
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

    def test_get_game_based_channel(self):
        expected = self.channel
        result = GameBasedChannelsManager.get_game_based_channel(self.session, self.game.steam_id)
        self.assertEqual(result, expected)
