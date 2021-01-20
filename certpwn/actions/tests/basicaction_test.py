# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from certpwn.actions import BasicAction


class TestBasicAction(unittest.TestCase):

    def setUp(self):
        self.action = BasicAction()

    def test_name(self):
        """Make sure the action has the correct name"""
        self.assertEqual("BasicAction", self.action.name)

    def test_perform(self):
        """Test if calling perform will raise a NotImplementedError"""
        update = Mock()
        with self.assertRaises(NotImplementedError):
            self.action.perform(update)


if __name__ == '__main__':
    unittest.main()
