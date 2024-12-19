import unittest
from unittest import mock

from certleak.actions.basicaction import BasicAction
from certleak.analyzers import AuthorityKeyIDAnalyzer


class TestAuthorityKeyIDAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AuthorityKeyIDAnalyzer(None, "keyid:14:2E:B3:17:B7:58:56:CB:AE:50:09:40:E6:1F:AF:9D:8B:14:C2:C6")
        self.update = mock.Mock()

    def test_match(self):
        """Check if AuthorityKeyIDAnalyzer matches the authorityKeyIdentifier"""
        self.update.extensions.authorityKeyIdentifier = "keyid:14:2E:B3:17:B7:58:56:CB:AE:50:09:40:E6:1F:AF:9D:8B:14:C2:C6"
        self.assertTrue(self.analyzer.match(self.update))

        self.update.extensions.authorityKeyIdentifier = None
        self.assertFalse(self.analyzer.match(self.update))

        self.update.extensions.authorityKeyIdentifier = ""
        self.assertFalse(self.analyzer.match(self.update))

        self.update = None
        self.assertFalse(self.analyzer.match(self.update))

    def test_actions_present(self):
        """Check if the actions are stored for the AlwaysTrueAnalyzer"""
        action = mock.MagicMock(spec=BasicAction)
        analyzer = AuthorityKeyIDAnalyzer(action, "SomeKey")
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
