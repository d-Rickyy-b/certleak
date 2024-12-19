import re

from .basicanalyzer import BasicAnalyzer


class RegexDomainAnalyzer(BasicAnalyzer):
    """Analyzer for using regex to find certificate updates for domains matching the pattern."""

    name = "RegexDomainAnalyzer"

    def __init__(self, actions, pattern, flags=0):
        """Analyzer for using regex to find certificate updates for domains matching the pattern.

        :param actions:
        :param pattern: pattern to match a certain domain name
        :param flags: the flags found in the 're' module
        """
        super().__init__(actions)
        self.regex = re.compile(pattern, flags)

    def match(self, update):
        """Match the domains of a cert update against the given regex."""
        if not update or not update.all_domains:
            return False

        matches = []

        for domain in update.all_domains:
            match = self.regex.findall(domain)
            matches += match

        if len(matches) > 0:
            return matches

        return False
