# -*- coding: utf-8 -*-
from .certstreamobject import CertstreamObject
from .extensions import Extensions
from .subject import Subject


class LeafCert(CertstreamObject):
    """Data class for the LeafCert data structure of certstream"""

    def __init__(self, subject, extensions, not_before, not_after, serial_number, fingerprint, as_der, all_domains):
        """
        Data class for the LeafCert data structure of certstream
        :param subject: Certificate subject
        :param extensions: Certificate extensions
        :param not_before: 'Not before' validity field
        :param not_after: 'Not after' validity field
        :param serial_number: Serial number of the certificate
        :param fingerprint: Certificate fingerprint
        :param as_der: DER representation of the certificate
        :param all_domains: List of all domains contained in this cert
        """
        super().__init__()
        self.subject = subject
        self.extensions = extensions
        self.not_before = not_before
        self.not_after = not_after
        self.serial_number = serial_number
        self.fingerprint = fingerprint
        self.as_der = as_der
        self.all_domains = all_domains

    @classmethod
    def from_dict(cls, data):
        """
        Create a LeafCert object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super(LeafCert, cls).from_dict(data)
        subject = Subject.from_dict(data.get("subject"))
        extensions = Extensions.from_dict(data.get("extensions"))
        not_before = data.get("not_before")
        not_after = data.get("not_after")
        serial_number = data.get("serial_number")
        fingerprint = data.get("fingerprint")
        as_der = data.get("as_der")
        all_domains = data.get("all_domains")

        return cls(subject=subject,
                   extensions=extensions,
                   not_before=not_before,
                   not_after=not_after,
                   serial_number=serial_number,
                   fingerprint=fingerprint,
                   as_der=as_der,
                   all_domains=all_domains)

    def __repr__(self):
        return f"(subject: {self.subject}, extensions: {self.extensions}, not_before: {self.not_before}, not_after: {self.not_after}, serial_number: " \
               f"{self.serial_number}, fingerprint: {self.fingerprint}, all_domains: {self.all_domains})"
