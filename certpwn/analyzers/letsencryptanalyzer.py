# -*- coding: utf-8 -*-

from .cafingerprintanalyzer import CAFingerprintAnalyzer


class LetsEncryptAnalyzer(CAFingerprintAnalyzer):
    """
    Analyzer for finding certificate updates that are signed by Let's Encrypt
    """
    name = "LetsEncryptAnalyzer"

    def __init__(self, actions=None):
        super().__init__(actions, fingerprint="E6:A3:B4:5B:06:2D:50:9B:33:82:28:2D:19:6E:FE:97:D5:95:6C:CB")
