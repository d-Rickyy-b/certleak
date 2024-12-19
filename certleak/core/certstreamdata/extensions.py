from .certstreamobject import CertstreamObject


class Extensions(CertstreamObject):
    """Data class representing the certificate extensions"""

    def __init__(self, keyUsage, extendedKeyUsage, basicConstraints, subjectKeyIdentifier, authorityKeyIdentifier, authorityInfoAccess, subjectAltName,
                 certificatePolicies, ctlSignedCertificateTimestamp):
        """
        Data class representing the certificate extensions
        :param keyUsage: keyUsage extension
        :param extendedKeyUsage: extendedKeyUsage extension
        :param basicConstraints: basicConstraints extension
        :param subjectKeyIdentifier: subjectKeyIdentifier extension
        :param authorityKeyIdentifier: authorityKeyIdentifier extension
        :param authorityInfoAccess: authorityInfoAccess extension
        :param subjectAltName: subjectAltName extension
        :param certificatePolicies: certificatePolicies extension
        :param ctlSignedCertificateTimestamp: ctlSignedCertificateTimestamp extension
        """
        super().__init__()
        self.keyUsage = keyUsage
        self.extendedKeyUsage = extendedKeyUsage
        self.basicConstraints = basicConstraints
        self.subjectKeyIdentifier = subjectKeyIdentifier
        self.authorityKeyIdentifier = authorityKeyIdentifier
        self.authorityInfoAccess = authorityInfoAccess
        self.subjectAltName = subjectAltName
        self.certificatePolicies = certificatePolicies
        self.ctlSignedCertificateTimestamp = ctlSignedCertificateTimestamp

    @classmethod
    def from_dict(cls, data):
        """
        Create an Extensions object from a dict
        :param data: dictionary data type containing the necessary data
        :return:
        """
        if not data:
            return None

        data = super(Extensions, cls).from_dict(data)
        keyUsage = data.get("keyUsage")
        extendedKeyUsage = data.get("extendedKeyUsage")
        basicConstraints = data.get("basicConstraints")
        subjectKeyIdentifier = data.get("subjectKeyIdentifier")
        authorityKeyIdentifier = data.get("authorityKeyIdentifier")
        authorityInfoAccess = data.get("authorityInfoAccess")
        subjectAltName = data.get("subjectAltName")
        certificatePolicies = data.get("certificatePolicies")
        ctlSignedCertificateTimestamp = data.get("ctlSignedCertificateTimestamp")

        return cls(keyUsage=keyUsage,
                   extendedKeyUsage=extendedKeyUsage,
                   basicConstraints=basicConstraints,
                   subjectKeyIdentifier=subjectKeyIdentifier,
                   authorityKeyIdentifier=authorityKeyIdentifier,
                   authorityInfoAccess=authorityInfoAccess,
                   subjectAltName=subjectAltName,
                   certificatePolicies=certificatePolicies,
                   ctlSignedCertificateTimestamp=ctlSignedCertificateTimestamp)

    def __repr__(self):
        return f"keyUsage: {self.keyUsage}, extendedKeyUsage: {self.extendedKeyUsage}, basicContstraints: {self.basicConstraints}, subjectKeyIdentifier: " \
               f"{self.subjectKeyIdentifier}, authorityKeyIdentifier: {self.authorityKeyIdentifier}, subjectAltName: {self.subjectAltName}, " \
               f"certificatePolicies: {self.certificatePolicies}, ctlSignedCertificateTimestamp: {self.ctlSignedCertificateTimestamp}"
