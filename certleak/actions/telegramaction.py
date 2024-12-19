import logging
import re

from certleak.util import Request, TemplatingEngine

from .basicaction import BasicAction


class TelegramAction(BasicAction):
    """Action to send a Telegram message to a certain user or group/channel."""

    name = "TelegramAction"

    def __init__(self, token, receiver, template=None):
        """Action to send a Telegram message to a certain user or group/channel.

        :param token: The Telegram API token for your bot obtained by @BotFather
        :param receiver: The userID/groupID or channelID of the receiving entity
        :param template: A template string describing how the update variables should be filled in.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if token is None or not re.match(r"[0-9]+:[a-zA-Z0-9\-_]+", token):
            msg = "Bot token not correct or None!"
            raise ValueError(msg)

        self.token = token
        self.receiver = receiver
        self.template = template

    def perform(self, update, analyzer_name=None, matches=None):
        """Send a message via a Telegram bot to a specified user, without checking for errors."""
        r = Request()
        text = TemplatingEngine.fill_template(update, analyzer_name, template_string=self.template, matches=matches)

        api_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.receiver}&text={text}"
        r.get(api_url)
