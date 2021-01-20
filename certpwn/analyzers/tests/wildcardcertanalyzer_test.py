# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch

from certpwn.analyzers import WildcardCertAnalyzer


class WildcardCertAnalyzerTest(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.analyzer = WildcardCertAnalyzer(None)

    def test_None(self):
        """Check if an empty list of domains returns False"""
        update = None
        self.assertFalse(self.analyzer.match(update))

    def test_empty_domain_list(self):
        """Check if an empty list of domains returns False"""
        update = Mock()
        update.all_domains = []
        self.assertFalse(self.analyzer.match(update))

    def test_no_wildcard(self):
        """Check if a list of non-wildcard domains returns False"""
        update = Mock()
        update.all_domains = ["test.de", "example.com", "subdomain.example.com"]
        self.assertFalse(self.analyzer.match(update))

    def test_no_domain(self):
        """Check if a list of non-domains returns False"""
        update = Mock()
        update.all_domains = ["this is no domain", "idk, smth weird", "yes"]
        self.assertFalse(self.analyzer.match(update))

    def test_one_wildcard_mixed(self):
        """Check if a list with a single wildcard domain mixed with other domains returns True"""
        update = Mock()
        update.all_domains = ["test.de", "example.com", "subdomain.example.com", "*.example.com"]
        self.assertTrue(self.analyzer.match(update))

    def test_multiple_wildcards_mixed(self):
        """Check if a list with multiple wildcard domains mixed with other domains returns True"""
        update = Mock()
        update.all_domains = ["test.de", "example.com", "*.test.com", "subdomain.example.com", "*.example.com"]
        self.assertTrue(self.analyzer.match(update))

    def test_multiple_wildcards(self):
        """Check if a list with multiple wildcard domains with no other domains returns True"""
        update = Mock()
        update.all_domains = ["*.test.com", "*.example.com"]
        self.assertTrue(self.analyzer.match(update))

    def test_single_wildcard(self):
        """Check if a list with multiple wildcard domains with no other domains returns True"""
        update = Mock()
        update.all_domains = ["*.example.com"]
        self.assertTrue(self.analyzer.match(update))

    def test_blacklist_multiple(self):
        """Check if blacklisting multiple word works as intended"""
        self.analyzer = WildcardCertAnalyzer(None, blacklist=["example", "test"])
        update = Mock()
        update.all_domains = ["*.example.com", "*.test.com"]
        self.assertFalse(self.analyzer.match(update))

    def test_blacklist_single(self):
        """Check if blacklisting a single word works as intended"""
        self.analyzer = WildcardCertAnalyzer(None, blacklist=["example"])
        update = Mock()
        update.all_domains = ["*.example.com"]
        self.assertFalse(self.analyzer.match(update))

    def test_blacklist_valid_domain(self):
        """Check if blacklisting a single word but with a valid domain works as intended"""
        self.analyzer = WildcardCertAnalyzer(None, blacklist=["example"])
        update = Mock()
        update.all_domains = ["*.example.com", "*.test.com"]
        match = self.analyzer.match(update)
        self.assertTrue(match)

        self.assertEqual(len(match), 1)
        self.assertEqual(match[0], "*.test.com")

    def test_match_content(self):
        """Check if blacklisting a single word but with a valid domain works as intended"""
        update = Mock()
        update.all_domains = ["*.example.com", "*.test.com", "*.asdf.com"]
        match = self.analyzer.match(update)
        self.assertTrue(match)

        self.assertEqual(len(match), 3)
        self.assertIn("*.example.com", match)
        self.assertIn("*.test.com", match)
        self.assertIn("*.asdf.com", match)

    @patch("certpwn.analyzers.wildcardcertanalyzer.tldextract")
    def test_match_exception(self, tldextract_mock):
        """Check if exception in tldextract 'extract' method is handled correctly"""
        tldextract_mock.extract = Mock(side_effect=Exception("Test exception for tldextract"))

        update = Mock()
        update.all_domains = ["*.example.com", "*.test.com", "*.asdf.com"]

        # The extract method will raise an exception that must be catched
        matches = self.analyzer.match(update)
        tldextract_mock.extract.assert_called()
        self.assertFalse(matches)
        self.assertEqual(0, len(matches))


if __name__ == "__main__":
    unittest.main()
