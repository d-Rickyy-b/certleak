# -*- coding: utf-8 -*-

from .basicanalyzer import BasicAnalyzer


class X509Analyzer(BasicAnalyzer):
    """
    Analyzer for finding X509 certificate updates
    """
    name = "X509Analyzer"

    def __init__(self, actions=None):
        super().__init__(actions)

    def match(self, update):
        return update.update_type == "X509LogEntry"
