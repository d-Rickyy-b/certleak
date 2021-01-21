# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from certpwn.analyzers.basicanalyzer import BasicAnalyzer, MergedAnalyzer


class TestMergedAnalyzer(unittest.TestCase):
    class NewAnalyzer(BasicAnalyzer):
        """Test Analyzer for testing mergedAnalyzer"""

        def __init__(self, return_value):
            super().__init__(actions=None)
            self.return_value = return_value

        def match(self, update):
            """Match func"""
            return self.return_value

    def setUp(self):
        """Setup test case"""
        self.true_analyzer = self.NewAnalyzer(True)
        self.false_analyzer = self.NewAnalyzer(False)
        self.update_mock = Mock()
        self.update_mock.body = "This is a mock update"

    def test_and(self):
        """Check if logical and between analyzers works fine"""
        and_analyzer = self.true_analyzer & self.false_analyzer

        # One analyzer returns False, the other True, this should evaluate to False
        self.assertFalse(and_analyzer.match(self.update_mock))

        and_analyzer2 = self.true_analyzer & self.true_analyzer
        # Since both analyzers return true, this should now return True as well
        self.assertTrue(and_analyzer2.match(self.update_mock))

    def test_or(self):
        """Check if logical or between analyzers works fine"""
        # One analyzer returns False, the other True, this should evaluate to True
        or_analyzer = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer.match(self.update_mock))

        # Since both return true, this should return True as well
        or_analyzer2 = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer2.match(self.update_mock))

        or_analyzer3 = self.false_analyzer | self.true_analyzer
        self.assertTrue(or_analyzer3.match(self.update_mock))

    def test_both(self):
        """Check if logical and/or both work fine in combination with each other"""
        # One analyzer returns False, the other True, this should evaluate to False
        and_analyzer = self.true_analyzer & self.false_analyzer
        self.assertFalse(and_analyzer.match(self.update_mock))

        # Since both return true, this should return True as well
        or_analyzer = self.true_analyzer | self.false_analyzer
        self.assertTrue(or_analyzer.match(self.update_mock))

    def test_not(self):
        """Check if inversion of analyzers works fine"""
        not_analyzer = ~self.true_analyzer
        self.assertFalse(not_analyzer.match(self.update_mock))

        not_analyzer = ~self.false_analyzer
        self.assertTrue(not_analyzer.match(self.update_mock))

    def test_none(self):
        """Check that error is raised in case no value is given for and/or/not_analyzer"""
        with self.assertRaises(ValueError):
            MergedAnalyzer(base_analyzer=None)

    def test_long_chain(self):
        """Check if logical and/or both work fine in long combinations with each other"""
        # Long chain of true_analyzers must evaluate to True
        and_analyzer = self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer & \
                       self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer
        self.assertTrue(and_analyzer.match(self.update_mock))

        # A single false_analyzer must make the term evaluate to false
        and_analyzer2 = self.true_analyzer & self.true_analyzer & self.true_analyzer & self.false_analyzer & \
                        self.true_analyzer & self.true_analyzer & self.true_analyzer & self.true_analyzer
        self.assertFalse(and_analyzer2.match(self.update_mock))

        # Since one returns true, this should return True as well
        or_analyzer = self.false_analyzer | self.false_analyzer | self.false_analyzer | self.false_analyzer | \
                      self.false_analyzer | self.true_analyzer | self.true_analyzer | self.true_analyzer
        self.assertTrue(or_analyzer.match(self.update_mock))

    def test_list_and(self):
        """Check if other return values than booleans are handled correctly with logical and"""
        and_analyzer = self.NewAnalyzer(["Test", 123]) & self.NewAnalyzer([])
        res = and_analyzer.match(self.update_mock)
        self.assertIsInstance(res, bool)
        self.assertFalse(res)

    def test_list_or(self):
        """Check if other return values than booleans are handled correctly with logical or"""
        and_analyzer = self.NewAnalyzer(["Test", 123]) | self.NewAnalyzer([])
        res = and_analyzer.match(self.update_mock)
        self.assertIsInstance(res, bool)
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()
