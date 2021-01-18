# -*- coding: utf-8 -*-
import re
import unittest
from unittest.mock import Mock

from certpwn.analyzers import DomainRegexAnalyzer


class TestDomainRegexAnalyzer(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.update = Mock()
        self.path_mock = Mock()
        self.path_mock.exists = Mock(return_value=True)
        self.analyzer = DomainRegexAnalyzer(actions=None, pattern="")

    def test_match_negative(self):
        """Check if the regex analyzer returns no results if the pattern doesn't match"""
        self.analyzer.pattern = r"^www\..*"
        self.update.all_domains = ["test.com", "subdomain.example.com"]
        matches = self.analyzer.match(self.update)

        self.assertFalse(matches)

    def test_match_positive(self):
        """Check if the regex analyzer returns correct results"""
        self.analyzer.pattern = r"^www\..*"
        self.update.all_domains = ["www.test.com", "subdomain.example.com"]
        matches = self.analyzer.match(self.update)

        self.assertTrue(matches)
        self.assertEqual(1, len(matches))
        self.assertEqual("www.test.com", matches[0])

    def test_match_positive_multiple(self):
        """Check if the regex analyzer returns multiple correct results"""
        self.analyzer.pattern = r"^www\..*"
        self.update.all_domains = ["www.test.com", "subdomain.example.com", "www.example.com"]
        matches = self.analyzer.match(self.update)

        self.assertTrue(matches)
        self.assertEqual(2, len(matches))
        self.assertEqual("www.test.com", matches[0])
        self.assertEqual("www.example.com", matches[1])

    def test_match_empty_domains(self):
        """Check if the regex analyzer returns False for an empty list of domains"""
        self.analyzer.pattern = r"^www\..*"
        self.update.all_domains = []
        matches = self.analyzer.match(self.update)

        self.assertFalse(matches)

    def test_match_domains_None(self):
        """Check if the regex analyzer returns False for a None-type update"""
        self.analyzer.pattern = r"^www\..*"
        self.update = None
        matches = self.analyzer.match(self.update)

        self.assertFalse(matches)

    def test_flags(self):
        """Test some regex flags. Not all, because as long as we use the re module, this should work fine"""
        self.analyzer.pattern = r"ThIsiSmIxEd\.com"
        self.update.all_domains = ["thisismixed.com"]
        self.assertFalse(self.analyzer.match(self.update), "The regex does match, although it shouldn't!")

        # Test case independend flag / ignorecase
        self.analyzer = DomainRegexAnalyzer(None, r"ThIsiSmIxEd\.com", flags=re.IGNORECASE)
        self.update.all_domains = ["thisismixed.com"]
        self.assertTrue(self.analyzer.match(self.update), "The regex does not match, although it should!")

        self.analyzer = DomainRegexAnalyzer(None, r"thisismixed\.com", flags=re.IGNORECASE)
        self.update.all_domains = ["ThIsiSmIxEd.com"]
        self.assertTrue(self.analyzer.match(self.update), "The regex does not match, although it should!")

    def test_set_pattern(self):
        """Check if changing the pattern works fine"""
        self.assertEqual("", self.analyzer.pattern)
        self.analyzer.pattern = r"[a-zA-Z0-9]\.(com)"

        self.assertEqual(r"[a-zA-Z0-9]\.(com)", self.analyzer.pattern)


if __name__ == "__main__":
    unittest.main()
