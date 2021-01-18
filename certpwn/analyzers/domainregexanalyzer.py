# -*- coding: utf-8 -*-
import re

from .basicanalyzer import BasicAnalyzer


class DomainRegexAnalyzer(BasicAnalyzer):
    """Analyzer for matching certificate domains against a regex"""
    name = "DomainRegexAnalyzer"

    def __init__(self, actions, pattern, flags=0):
        """Analyzer for matching certificate domains against a regex

        :param actions: A single action or a list of actions to be executed on every update
        :param pattern: The pattern to match the domains against
        :param flags: Flags for the re.compile method
        """
        super().__init__(actions)
        self._pattern = pattern
        self.flags = flags
        self.regex = re.compile(pattern, flags)

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.regex = re.compile(pattern=value, flags=self.flags)

    def match(self, update):
        """Check if any of the certificate domain names are contained in the list of generated pot. phishing domains

        :param update: An update object which should be matched
        :return: `bool` if the update has been matched
        """
        if update is None:
            return []

        matches = []
        for domain in update.all_domains:
            matches += self.regex.findall(domain)

        return matches
