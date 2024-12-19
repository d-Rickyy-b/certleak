
from .basicanalyzer import BasicAnalyzer


class PreCertAnalyzer(BasicAnalyzer):
    """
    Analyzer for finding pre certificate updates
    """
    name = "PreCertAnalyzer"

    def __init__(self, actions=None):
        super().__init__(actions)

    def match(self, update):
        return update.update_type == "PrecertLogEntry"
