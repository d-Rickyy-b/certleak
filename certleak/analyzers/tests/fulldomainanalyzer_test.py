# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from certleak.actions.basicaction import BasicAction
from certleak.analyzers import FullDomainAnalyzer


class TestFullDomainAnalyzer(unittest.TestCase):
    def setUp(self):
        self.update = mock.Mock()
        self.action = mock.MagicMock(spec=BasicAction)

    def test_setup(self):
        """Check if the word list is initialized correctly"""
        analyzer = FullDomainAnalyzer(self.action, "test")
        self.assertEqual(1, len(analyzer.contained_words))
        self.assertEqual("test", analyzer.contained_words[0])

        analyzer = FullDomainAnalyzer(self.action, ["test", "123"])
        self.assertEqual(2, len(analyzer.contained_words))
        self.assertEqual("test", analyzer.contained_words[0])
        self.assertEqual("123", analyzer.contained_words[1])

    def test_single_word(self):
        """Check if the analyzer matches if passing a single word to it"""
        analyzer = FullDomainAnalyzer(self.action, "test")
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]
        self.assertTrue(analyzer.match(update))
        self.assertEqual(3, len(analyzer.match(update)))

        analyzer = FullDomainAnalyzer(self.action, "2.ex")
        self.assertTrue(analyzer.match(update))
        self.assertEqual(1, len(analyzer.match(update)))

        analyzer = FullDomainAnalyzer(self.action, "test2")
        self.assertTrue(analyzer.match(update))

        analyzer = FullDomainAnalyzer(self.action, "mytest")
        self.assertFalse(analyzer.match(update))

    def test_empty_string(self):
        """Check if the analyzer matches if the matched word is an empty string"""
        analyzer = FullDomainAnalyzer(self.action, "")

        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]

        self.assertFalse(analyzer.match(update))

        analyzer = FullDomainAnalyzer(self.action, [""])

        self.assertFalse(analyzer.match(update))

    def test_none_update(self):
        """Check if the analyzer matches if the update object is None"""
        analyzer = FullDomainAnalyzer(self.action, "test")
        update = None
        self.assertFalse(analyzer.match(update))
        self.assertEqual(0, len(analyzer.match(update)))

    def test_empty_update_domains(self):
        """Check if the analyzer matches if the list of domains is empty"""
        analyzer = FullDomainAnalyzer(self.action, "test")
        update = mock.Mock()
        update.all_domains = []
        self.assertFalse(analyzer.match(update))
        self.assertEqual(0, len(analyzer.match(update)))

    def test_multiple_words(self):
        """Test if the analyzer matches multiple words correctly"""
        analyzer = FullDomainAnalyzer(self.action, ["test", "example"])
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]
        self.assertTrue(analyzer.match(update))
        self.assertEqual(3, len(analyzer.match(update)))  # We still expect 3 results, because we are returning domains

        analyzer = FullDomainAnalyzer(self.action, ["Nothing", "Matches"])
        self.assertFalse(analyzer.match(update))
        self.assertEqual(0, len(analyzer.match(update)))

        analyzer = FullDomainAnalyzer(self.action, ["Nothing", "Matches", "anotherone", "ThisIsFun", "nosubdomain", "lastone"])
        self.assertTrue(analyzer.match(update))
        self.assertEqual(1, len(analyzer.match(update)))

    def test_actions_present(self):
        """Check if the action passed to the analyzer is being stored"""
        action = mock.MagicMock(spec=BasicAction)
        analyzer = FullDomainAnalyzer(action)
        self.assertEqual([action], analyzer.actions)

    def test_exact_match(self):
        """Check if the analyzer matches if passing a single domain to it using the exact_match param"""
        analyzer = FullDomainAnalyzer(self.action, "test", exact_match=True)
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]
        matches = analyzer.match(update)
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))

        analyzer = FullDomainAnalyzer(self.action, "test.example.com", exact_match=True)
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]
        matches = analyzer.match(update)
        self.assertTrue(matches)
        self.assertEqual(1, len(matches))
        self.assertEqual("test.example.com", matches[0])


if __name__ == "__main__":
    unittest.main()
