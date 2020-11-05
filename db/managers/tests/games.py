import unittest

from db.instance import DBInstance
from db.managers.games import GamesManager
from db.managers.tests import init_test_session
from db.models import Game
from db.models.base import Base


class TestGamesManager(unittest.TestCase):
    def setUp(self):
        self.session = init_test_session()
        self.game1 = Game(name='test game', steam_id=0)
        self.game2 = Game(name='test game 2', steam_id=2)

        self.session.add(self.game1)
        self.session.add(self.game2)
        self.session.commit()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(DBInstance.engine())

    def test_get_all(self):
        games = GamesManager.get_all(self.session)
        self.assertEqual(len(games), 2)
