import pickle
import unittest

from scrapper.updater import Updater


class UpdaterTest(unittest.TestCase):

    def test_start(self):
        assert True

    def test_register_observer(self):
        assert True

    def test_unregister_observer(self):
        assert True

    def test_load_updates(self):
        with open('test_load_updates_excepted_value.txt', 'rb') as file:
            excepted_value = pickle.load(file)
        self.assertListEqual(excepted_value, Updater.load_updates(1097150))

    def test_load_updates_raise_exception(self):
        with self.assertRaises(Exception) as EXCEPTION:
            Updater.load_updates(111)
        self.assertTrue('rss feed doesn`t exist' in str(EXCEPTION.exception))
