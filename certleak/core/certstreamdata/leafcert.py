from .certstreamobject import CertstreamObject
from .extensions import Extensions
from .subject import Subject


class LeafCert(CertstreamObject):
    """Data class for the LeafCert data structure of certstream"""

    def __init__(self, subject, issuer, extensions, not_before, not_after, serial_number, fingerprint, signature_algorithm, all_domains, as_der):
        """
        Data class for the LeafCert data structure of certstream
        :param subject: Certificate subject
        :param extensions: Certificate extensions
        :param not_before: 'Not before' validity field
        :param not_after: 'Not after' validity field
        :param serial_number: Serial number of the certificate
        :param fingerprint: Certificate fingerprint
        :param signature_algorithm: Signature algorithm
        :param all_domains: List of all domains contained in this cert
        :param as_der: DER (Distinguished Encoding Rules) encoded binary representation of the certificate, only
                    available for the /full-stream endpoint. Will be None otherwise.
        """
        super().__init__()
        self.subject = subject
        self.issuer = issuer
        self.extensions = extensions
        self.not_before = not_before
        self.not_after = not_after
        self.serial_number = serial_number
        self.fingerprint = fingerprint
        self.signature_algorithm = signature_algorithm
        self.all_domains = all_domains
        self.as_der = as_der

    @classmethod
    def from_dict(cls, data):
        """
        Create a LeafCert object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super().from_dict(data)
        subject = Subject.from_dict(data.get("subject"))
        issuer = Subject.from_dict(data.get("issuer"))
        extensions = Extensions.from_dict(data.get("extensions"))
        not_before = data.get("not_before")
        not_after = data.get("not_after")
        serial_number = data.get("serial_number")
        fingerprint = data.get("fingerprint")
        all_domains = data.get("all_domains")
        signature_algorithm = data.get("signature_algorithm")
        as_der = data.get("as_der")

        return cls(
            subject=subject,
            issuer=issuer,
            extensions=extensions,
            not_before=not_before,
            not_after=not_after,
            serial_number=serial_number,
            fingerprint=fingerprint,
            signature_algorithm=signature_algorithm,
            all_domains=all_domains,
            as_der=as_der,
        )

    def __repr__(self):
        return f"(subject: {self.subject}, issuer: {self.issuer}, extensions: {self.extensions}, not_before: {self.not_before}, not_after: {self.not_after}, serial_number: {self.serial_number}, fingerprint: {self.fingerprint}, all_domains: {self.all_domains}, as_der: {self.as_der})"
