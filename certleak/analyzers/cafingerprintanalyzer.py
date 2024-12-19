from .basicanalyzer import BasicAnalyzer


class CAFingerprintAnalyzer(BasicAnalyzer):
    """Analyzer for finding certificate updates that are signed by a CA with a specified fingerprint."""

    name = "CAFingerprintAnalyzer"

    def __init__(self, actions, fingerprint):
        """
        Find a CA with a specific fingerprint
        :param actions:
        :param fingerprint: Certificate fingerprint, bytes separated by colons
        """
        super().__init__(actions)
        self.fingerprint = fingerprint

    def match(self, update):
        # TODO chain doesn't work!
        return any(cert.extensions.basicConstraints == "CA:TRUE" and cert.fingerprint.lower() == self.fingerprint.lower() for cert in update.chain)
