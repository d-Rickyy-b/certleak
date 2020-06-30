# -*- coding: utf-8 -*-
from .certstreamobject import CertstreamObject
from .chain import Chain
from .leafcert import LeafCert


class Update(CertstreamObject):
    """Data class for the certificate Update type from certstream"""

    def __init__(self, update_type, leaf_cert, chain, cert_index, seen, source):
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
        self.chain = chain
        self.cert_index = cert_index
        self.seen = seen
        self.source = source
        self.all_domains = leaf_cert.all_domains

    @classmethod
    def from_dict(cls, data):
        """
        Create an Update object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super(Update, cls).from_dict(data)
        update_type = data.get("update_type")
        leaf_cert = LeafCert.from_dict(data.get("leaf_cert"))
        chain = Chain.from_dict(data.get("chain"))
        cert_index = data.get("cert_index")
        seen = data.get("seen")
        source = data.get("source")

        return cls(update_type=update_type,
                   leaf_cert=leaf_cert,
                   chain=chain,
                   cert_index=cert_index,
                   seen=seen,
                   source=source)

    def __repr__(self):
        return f"(update_type: {self.update_type}, leaf_cert: {self.leaf_cert}, chain: {self.chain}, cert_index: {self.cert_index}, seen: {self.seen}, " \
               f"source: {self.source})"