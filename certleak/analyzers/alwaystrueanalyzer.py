from .basicanalyzer import BasicAnalyzer


class AlwaysTrueAnalyzer(BasicAnalyzer):
    """Analyzer which always matches an certificate update to perform actions on every certificate update"""

    name = "AlwaysTrueAnalyzer"

    def __init__(self, actions):
        """
        Analyzer which always matches a certificate update to perform actions on every certificate update
        :param actions: A single action or a list of actions to be executed on every certificate update
        """
        super().__init__(actions)

    def match(self, update):
        """Always returns True to match every update available"""
        return True
