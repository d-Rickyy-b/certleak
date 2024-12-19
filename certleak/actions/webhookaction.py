import logging

from certleak.util import Request

from .basicaction import BasicAction


class WebhookAction(BasicAction):
    """Action to perform a Webhook on a matched update"""
    name = "WebhookAction"
    logger = logging.getLogger(__name__)

    def __init__(self, url, post_data=True):
        """
        Init method for the WebhookAction
        :param url: string, URL to POST against
        :param post_data: boolean, to decide wheather a update should be sent in the body
        """
        super().__init__()
        self.url = url
        self.post_data = post_data

    def perform(self, update, analyzer_name=None, matches=None):
        """
        Trigger the webhook
        :param update: The update passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the update
        :param matches: List of matches returned by the analyzer
        :return: None
        """
        if update is None:
            self.logger.warning("Update is None!")
            return

        update_dict = update.to_dict() if self.post_data else None

        r = Request()
        r.post(url=self.url, data=update_dict)
