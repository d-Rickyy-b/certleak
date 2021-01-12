# -*- coding: utf-8 -*-
from .certstreamobject import CertstreamObject
from .leafcert import LeafCert


class Update(CertstreamObject):
    """Data class for the certificate Update type from certstream"""

    def __init__(self, update_type, leaf_cert, cert_index, cert_link, seen, source, raw_dict):
        """
        Data class for the certificate Update type from certstream
        :param update_type: The type of the certificate update
        :param leaf_cert: The LeafCert object of this update
        :param chain: The cert Chain object of this update
        :param cert_index: The cert index of this update
        :param seen: When this certificate update has been seen
        :param source: The certificate transparency log this update is coming from
        """
        super().__init__()
        self.update_type = update_type
        self.leaf_cert = leaf_cert
        self.cert_index = cert_index
        self.cert_link = cert_link
        self.seen = seen
        self.source = source
        self.all_domains = leaf_cert.all_domains if leaf_cert is not None else ""
        self.raw_dict = raw_dict

    @classmethod
    def from_dict(cls, data):
        """
        Create an Update object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        raw_data = data.copy()
        data = super(Update, cls).from_dict(data)
        update_type = data.get("update_type")
        leaf_cert = LeafCert.from_dict(data.get("leaf_cert"))
        cert_index = data.get("cert_index")
        cert_link = data.get("cert_link")
        seen = data.get("seen")
        source = data.get("source")

        return cls(update_type=update_type,
                   leaf_cert=leaf_cert,
                   cert_index=cert_index,
                   cert_link=cert_link,
                   seen=seen,
                   source=source,
                   raw_dict=raw_data)

    def to_dict(self):
        return self.raw_dict

    def __repr__(self):
        return f"(update_type: {self.update_type}, leaf_cert: {self.leaf_cert}, chain: {self.cert_index}, cert_index: {self.cert_link}, seen: {self.seen}, " \
               f"source: {self.source})"
