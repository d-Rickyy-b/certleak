# -*- coding: utf-8 -*-

from .basicanalyzer import BasicAnalyzer


class LetsEncryptAnalyzer(BasicAnalyzer):
    """
    Analyzer for finding certificate updates that are signed by Let's Encrypt
    """
    name = "LetsEncryptAnalyzer"

    def __init__(self, actions=None):
        super().__init__(actions)

    def match(self, update):
        return "Let's Encrypt" == update.leaf_cert.issuer.O
