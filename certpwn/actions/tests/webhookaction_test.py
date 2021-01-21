# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from certpwn.actions.webhookaction import WebhookAction


class TestWebhookAction(unittest.TestCase):

    def setUp(self):
        self.url = "https://example.com"
        self.action = WebhookAction(url=self.url)

    def test_init(self):
        """Check if initialization works as intended"""
        self.assertEqual(self.action.url, self.url)
        self.assertEqual(self.action.post_data, True)

        self.action = WebhookAction(url=self.url, post_data=False)
        self.assertEqual(self.action.post_data, False)

    @patch("certpwn.actions.webhookaction.Request")
    def test_perform_data(self, request_mock):
        """Check that running perform with post_data set to True sends a webrequest to the specified webhook url"""
        update = Mock()
        update.to_dict = Mock(return_value="This is a test")
        analyzer_name = "name"
        matches = []

        request_object_mock = Mock()
        request_mock.return_value = request_object_mock

        self.action.perform(update, analyzer_name, matches)

        request_mock.assert_called_once()
        request_object_mock.post.assert_called_once_with(url=self.url, data="This is a test")
        update.to_dict.assert_called_once()

    @patch("certpwn.actions.webhookaction.Request")
    def test_perform_no_data(self, request_mock):
        """Check that running perform with post_data set to False sends a webrequest to the specified webhook url"""
        self.action = WebhookAction(url=self.url, post_data=False)

        update = Mock()
        analyzer_name = "name"
        matches = []

        request_object_mock = Mock()
        request_mock.return_value = request_object_mock

        self.action.perform(update, analyzer_name, matches)

        request_mock.assert_called_once()
        request_object_mock.post.assert_called_once_with(url=self.url, data=None)
        update.to_dict.assert_not_called()

    @patch("certpwn.actions.webhookaction.Request")
    def test_perform_None(self, request_mock):
        """Check that passing None as update will not actually post the webhook"""
        update = None
        analyzer_name = "name"
        matches = []

        request_object_mock = Mock()
        request_mock.return_value = request_object_mock

        self.action.perform(update, analyzer_name, matches)

        request_mock.assert_not_called()
        request_object_mock.post.assert_not_called()


if __name__ == '__main__':
    unittest.main()
