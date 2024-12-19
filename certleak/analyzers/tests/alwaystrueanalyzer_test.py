import unittest
from unittest import mock

from certleak.actions.basicaction import BasicAction
from certleak.analyzers import AlwaysTrueAnalyzer


class TestAlwaysTrueAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = AlwaysTrueAnalyzer(None)
        self.update = mock.Mock()

    def test_match(self):
        """Check if AlwaysTrueAnalyzer returns always True"""
        self.update.body = "Test"
        self.assertTrue(self.analyzer.match(self.update))

        self.update.body = None
        self.assertTrue(self.analyzer.match(self.update))

        self.update.body = ""
        self.assertTrue(self.analyzer.match(self.update))

        self.update = None
        self.assertTrue(self.analyzer.match(self.update))

    def test_actions_present(self):
        """Check if the actions are stored for the AlwaysTrueAnalyzer"""
        action = mock.MagicMock(spec=BasicAction)
        analyzer = AlwaysTrueAnalyzer(action)
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
