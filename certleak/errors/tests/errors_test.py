# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from certleak.errors.errors import CertleakError


class TestErrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_CertleakError(self):
        """Test if the CertleakError returns its string message"""
        msg = "This is a test message"
        error = CertleakError(msg)
        self.assertEqual(msg, error.message)
        self.assertEqual(msg, str(error))

        mock = Mock()
        mock.__str__ = Mock(return_value="This is just another test message")
        error = CertleakError(mock)
        self.assertEqual(mock, error.message)
        self.assertEqual(str(mock), str(error))


if __name__ == "__main__":
    unittest.main()
