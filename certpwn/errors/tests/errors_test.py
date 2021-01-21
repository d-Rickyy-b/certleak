# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from certpwn.errors.errors import CertpwnError


class TestErrors(unittest.TestCase):
    def setUp(self):
        pass

    def test_CertpwnError(self):
        """Test if the CertpwnError returns its string message"""
        msg = "This is a test message"
        error = CertpwnError(msg)
        self.assertEqual(msg, error.message)
        self.assertEqual(msg, str(error))

        mock = Mock()
        mock.__str__ = Mock(return_value="This is just another test message")
        error = CertpwnError(mock)
        self.assertEqual(mock, error.message)
        self.assertEqual(str(mock), str(error))


if __name__ == "__main__":
    unittest.main()
