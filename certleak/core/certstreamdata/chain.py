from .certstreamobject import CertstreamObject
from .leafcert import LeafCert


class Chain(CertstreamObject):
    """Data class representing a certificate chain."""

    def __init__(self, cert_list):
        """
        Data class representing a certificate chain
        :param cert_list: List of parent certificates used to create the actual certificate of the Update.
        """
        super().__init__()
        self._chain = cert_list
        self._index = 0

    @classmethod
    def from_dict(cls, data):
        """
        Create a Chain object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super().from_dict(data)
        cert_list = []

        for cert in data:
            c = LeafCert.from_dict(cert)
            cert_list.append(c)

        return cls(cert_list=cert_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._chain):
            result = self._chain[self._index]
            self._index += 1
            return result
        self._index = 0
        raise StopIteration

    def __repr__(self):
        return f"{self._chain}"
