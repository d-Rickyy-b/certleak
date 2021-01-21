# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from certpwn.actions.basicaction import BasicAction
from certpwn.analyzers import SubDomainAnalyzer


class TestSubDomainAnalyzer(unittest.TestCase):
    def setUp(self):
        self.update = mock.Mock()
        self.action = mock.MagicMock(spec=BasicAction)

    def test_setup(self):
        """Check if the word list is initialized correctly"""
        analyzer = SubDomainAnalyzer(self.action, "test")
        self.assertEqual("test", analyzer.subdomains[0])
        self.assertEqual(True, analyzer.exact_match)

        analyzer = SubDomainAnalyzer(self.action, "test2", exact_match=False)
        self.assertEqual("test2", analyzer.subdomains[0])
        self.assertEqual(False, analyzer.exact_match)

    def test_single_word_exact(self):
        """Check if the analyzer matches in "exact" mode if passing a single word to it"""
        analyzer = SubDomainAnalyzer(self.action, "test", exact_match=True)
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]
        matches = analyzer.match(update)
        self.assertTrue(matches)
        self.assertEqual(2, len(matches))
        self.assertIn("test.example.com", matches)
        self.assertIn("test.beispiel.de", matches)

        analyzer = SubDomainAnalyzer(self.action, "test2")
        matches = analyzer.match(update)
        self.assertTrue(matches)
        self.assertEqual(1, len(matches))
        self.assertEqual("test2.example.com", matches[0])

        analyzer = SubDomainAnalyzer(self.action, "mytest")
        self.assertFalse(analyzer.match(update))

    def test_empty_string(self):
        """Check if the analyzer matches domains without subdomains if the subdomain param is an empty string"""
        analyzer = SubDomainAnalyzer(self.action, "")

        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "test.beispiel.de", "nosubdomain.de"]

        matches = analyzer.match(update)
        self.assertTrue(matches)
        self.assertEqual("nosubdomain.de", matches[0])

    def test_none_update(self):
        """Check if the analyzer matches if the update object is None"""
        analyzer = SubDomainAnalyzer(self.action, "test")
        update = None
        matches = analyzer.match(update)
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))

    def test_empty_update_domains(self):
        """Check if the analyzer matches if the list of domains is empty"""
        analyzer = SubDomainAnalyzer(self.action, "test")
        update = mock.Mock()
        update.all_domains = []
        matches = analyzer.match(update)
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))

    def test_multiple_words(self):
        """Test if the analyzer matches multiple words correctly"""
        analyzer = SubDomainAnalyzer(self.action, ["test", "example"])
        update = mock.Mock()
        update.all_domains = ["test.example.com", "test2.example.com", "example.beispiel.de", "nosubdomain.de"]
        matches = analyzer.match(update)
        self.assertTrue(matches)
        self.assertEqual(2, len(matches))
        self.assertIn("test.example.com", matches)
        self.assertIn("example.beispiel.de", matches)

        analyzer = SubDomainAnalyzer(self.action, ["Nothing", "Matches"])
        matches = analyzer.match(update)
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))

        analyzer = SubDomainAnalyzer(self.action, ["Nothing", "Matches", "anotherone", "ThisIsFun", "nosubdomain", "lastone"])
        matches = analyzer.match(update)
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))

    def test_actions_present(self):
        """Check if the action passed to the analyzer is being stored"""
        action = mock.MagicMock(spec=BasicAction)
        analyzer = SubDomainAnalyzer(action, "word")
        self.assertEqual([action], analyzer.actions)


if __name__ == "__main__":
    unittest.main()
