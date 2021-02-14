# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock

from certpwn.actions import BasicAction
from certpwn.analyzers import PreCertAnalyzer


class PreCertAnalyzerTest(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.analyzer = PreCertAnalyzer(None)

    def test_positive(self):
        """Check if analyzer matches updates of type PreCertAnalyzer"""
        update = Mock()
        update.update_type = "PrecertLogEntry"
        self.assertTrue(self.analyzer.match(update))

    def test_negative(self):
        """Check if analyzer doesn't match anything else"""
        update = Mock()
        update.update_type = "OtherEntry"
        self.assertFalse(self.analyzer.match(update))

    def test_actions(self):
        """Check if actions are set up properly"""
        action1 = Mock(spec=BasicAction)
        action2 = Mock(spec=BasicAction)
        self.analyzer = PreCertAnalyzer(action1)
        self.assertEqual(1, len(self.analyzer.actions))
        self.assertEqual(action1, self.analyzer.actions[0])

        self.analyzer = PreCertAnalyzer(actions=[action1, action2])
        self.assertEqual(2, len(self.analyzer.actions))
        self.assertIn(action1, self.analyzer.actions)
        self.assertIn(action2, self.analyzer.actions)


if __name__ == "__main__":
    unittest.main()
