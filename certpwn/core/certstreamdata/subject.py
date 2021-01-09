# -*- coding: utf-8 -*-
from .certstreamobject import CertstreamObject


class Subject(CertstreamObject):
    """Data class for the Subject field of a certificate"""

    def __init__(self, aggregated, c, st, l, o, ou, cn, email_address):
        """
        Data class for the Subject field of a certificate
        :param aggregated: Aggregated string of the other RDNs
        :param c: CountryName
        :param st: StateOrProvinceName
        :param l: Locality
        :param o: Organization
        :param ou: OrganizationalUnit
        :param cn: CommonName
        """
        super().__init__()
        self.aggregated = aggregated
        self.C = c
        self.ST = st
        self.L = l
        self.O = o
        self.OU = ou
        self.CN = cn
        self.email_address = email_address

    @classmethod
    def from_dict(cls, data):
        """
        Create a Subject object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super(Subject, cls).from_dict(data)
        aggregated = data.get("aggregated")
        c = data.get("c")
        st = data.get("ST")
        l = data.get("L")
        o = data.get("O")
        ou = data.get("OU")
        cn = data.get("CN")
        email_address = data.get("emailAddress")

        return cls(aggregated=aggregated, c=c, st=st, l=l, o=o, ou=ou, cn=cn, email_address=email_address)

    def __repr__(self):
        return "Subject(C='%s', ST='%s', L='%s', O='%s', OU='%s', CN='%s' | aggregated='%s')" % (self.C, self.ST, self.L, self.O, self.OU, self.CN,
                                                                                                 self.aggregated)
