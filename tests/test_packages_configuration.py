# -*- coding: utf8 -*-
from packages.configuration import Configuration
import unittest
import os


class ConfigurationTest(unittest.TestCase):

    def setUp(self):
        current_path = os.path.dirname(__file__)
        self.configuration_path = os.path.join(current_path, 'test_data', 'configuration')
        self.test_config = Configuration(self.configuration_path, 'test')

    def tearDown(self):
        pass

    def test_init(self):
        with self.assertRaises(RuntimeError):
            Configuration("/some_fantasy_path", 'name')
        with self.assertRaises(RuntimeError):
            Configuration(self.configuration_path, 'test_empty')

    def test_get_config_value(self):
        self.assertEqual(self.test_config.get('wrong_key'), None)
        self.assertEqual(self.test_config.get("first"), 'key')

if __name__=="__main__":
    unittest.main()