from .certstreamobject import CertstreamObject
from .update import Update


class Message(CertstreamObject):
    """Data class for the Message data structure of certstream"""

    def __init__(self, message_type, update):
        """
        Data class for the Message data structure of certstream
        :param message_type: Type of the message (e.g. 'heartbeat' or 'certificate_update')
        :param update: Actual certificate update (called 'data')
        """
        super().__init__()
        self.message_type = message_type
        self.update = update

    @classmethod
    def from_dict(cls, data):
        """
        Create a Message object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super().from_dict(data)
        message_type = data.get("message_type")
        update = Update.from_dict(data.get("data"))

        return cls(message_type=message_type, update=update)

    def __repr__(self):
        return ""
