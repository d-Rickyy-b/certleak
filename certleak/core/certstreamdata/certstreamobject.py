

class CertstreamObject:
    """Base class for all the certstream data classes"""

    @classmethod
    def from_dict(cls, data):
        """
        Returns a copy of the passed data
        :param data: The dict from which an object should be created from
        :return: copy of data or None
        """
        if not data:
            return None

        return data.copy()
