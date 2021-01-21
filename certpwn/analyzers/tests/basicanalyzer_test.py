# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from certpwn.actions import BasicAction
from certpwn.analyzers import BasicAnalyzer
from certpwn.errors import InvalidActionError


class TestBasicAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = BasicAnalyzer(None)

    def test_name(self):
        """Make sure the analyzer has the correct name"""
        self.assertEqual("BasicAnalyzer", self.analyzer.name)

    def test_init(self):
        """Check if the initialization process works as intended"""
        self.assertTrue(isinstance(self.analyzer.actions, list))
        self.assertEqual(0, len(self.analyzer.actions))

    def test_init_action(self):
        """Check if initialization with a single action works fine"""
        action = Mock(spec=BasicAction)
        self.analyzer = BasicAnalyzer(actions=action)
        self.assertTrue(isinstance(self.analyzer.actions, list))
        self.assertEqual(1, len(self.analyzer.actions))
        self.assertEqual(action, self.analyzer.actions[0])

    def test_init_actions(self):
        """Check if initialization with multiple actions works fine"""
        action1 = Mock(spec=BasicAction)
        action2 = Mock(spec=BasicAction)
        self.analyzer = BasicAnalyzer(actions=[action1, action2])
        self.assertTrue(isinstance(self.analyzer.actions, list))
        self.assertEqual(2, len(self.analyzer.actions))
        self.assertIn(action1, self.analyzer.actions)
        self.assertIn(action2, self.analyzer.actions)

    def test_add_action(self):
        """Check if adding a new action to the analyzer"""
        action1 = Mock(spec=BasicAction)
        self.analyzer.add_action(action1)

        self.assertEqual(1, len(self.analyzer.actions))

        action2 = Mock(spec=BasicAction)
        self.analyzer.add_action(action2)

        self.assertEqual(2, len(self.analyzer.actions))
        self.assertIn(action1, self.analyzer.actions)
        self.assertIn(action2, self.analyzer.actions)

    def test_match(self):
        """Test if calling match will raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.analyzer.match(Mock())

    @patch("certpwn.analyzers.basicanalyzer.MergedAnalyzer")
    def test_andanalyzer(self, mergedanalyzer_mock):
        """Check if using logical AND works as expected"""
        analyzer1 = BasicAnalyzer(None)
        analyzer2 = BasicAnalyzer(None)
        analyzer = analyzer1 & analyzer2

        mergedanalyzer_mock.assert_called_once_with(analyzer1, and_analyzer=analyzer2)
        self.assertEqual(mergedanalyzer_mock(), analyzer)

    @patch("certpwn.analyzers.basicanalyzer.MergedAnalyzer")
    def test_oranalyzer(self, mergedanalyzer_mock):
        """Check if using logical OR works as expected"""
        analyzer1 = BasicAnalyzer(None)
        analyzer2 = BasicAnalyzer(None)
        analyzer = analyzer1 | analyzer2

        mergedanalyzer_mock.assert_called_once_with(analyzer1, or_analyzer=analyzer2)
        self.assertEqual(mergedanalyzer_mock(), analyzer)

    @patch("certpwn.analyzers.basicanalyzer.MergedAnalyzer")
    def test_invertanalyzer(self, mergedanalyzer_mock):
        """Check if using inversion works as expected"""
        analyzer1 = BasicAnalyzer(None)
        analyzer = ~analyzer1

        mergedanalyzer_mock.assert_called_once_with(base_analyzer=None, not_analyzer=analyzer1)
        self.assertEqual(mergedanalyzer_mock(), analyzer)

    def test_repr(self):
        """Check if generating a representation of an analyzer works fine"""
        self.analyzer.identifier = "This is a test"
        self.assertEqual("This is a test", str(self.analyzer))

    def test_repr_none(self):
        """Check if generating a representation of an analyzer works fine if identifier is None"""
        self.analyzer.identifier = None
        self.assertEqual("BasicAnalyzer", str(self.analyzer))

    def test_repr_no_identifier(self):
        """Check if generating a representation of an analyzer works fine when no identifier is set"""
        self.analyzer.identifier = "This is a test"
        self.assertEqual("This is a test", str(self.analyzer))

    def test__check_action(self):
        """Check if passing something else than an instance of BasicAction to _check_action raises an error"""
        action = Mock()
        with self.assertRaises(InvalidActionError):
            self.analyzer._check_action(action)

    def test__check_action2(self):
        """Check if passing a reference to the BasicAction class to _check_action raises an error"""
        action = BasicAction
        with self.assertRaises(InvalidActionError):
            self.analyzer._check_action(action)


if __name__ == '__main__':
    unittest.main()
