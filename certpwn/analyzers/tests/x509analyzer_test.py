# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock

from certpwn.analyzers import X509Analyzer


class X509AnalyzerTest(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.analyzer = X509Analyzer(None)

    def test_positive(self):
        """Check if analyzer matches updates of type X509LogEntry"""
        update = Mock()
        update.update_type = "X509LogEntry"
        self.assertTrue(self.analyzer.match(update))

    def test_negative(self):
        """Check if analyzer doesn't match anything else"""
        update = Mock()
        update.update_type = "OtherEntry"
        self.assertFalse(self.analyzer.match(update))


if __name__ == "__main__":
    unittest.main()
