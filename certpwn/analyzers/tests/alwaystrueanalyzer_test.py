# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from certpwn.actions.basicaction import BasicAction
from certpwn.analyzers import AlwaysTrueAnalyzer


class TestAlwaysTrueAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AlwaysTrueAnalyzer(None)
        self.update = mock.Mock()

    def test_match(self):
        self.update.body = "Test"
        self.assertTrue(self.analyzer.match(self.update))

        self.update.body = None
        self.assertTrue(self.analyzer.match(self.update))

        self.update.body = ""
        self.assertTrue(self.analyzer.match(self.update))

        self.update = None
        self.assertTrue(self.analyzer.match(self.update))

    def test_actions_present(self):
        action = mock.MagicMock(spec=BasicAction)
        analyzer = AlwaysTrueAnalyzer(action)
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
