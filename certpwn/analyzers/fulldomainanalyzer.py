# -*- coding: utf-8 -*-
import logging

from certpwn.util import listify
from .basicanalyzer import BasicAnalyzer


class FullDomainAnalyzer(BasicAnalyzer):
    """Analyzer to match domains containing certain strings"""
    name = "FullDomainAnalyzer"
    logger = logging.getLogger(__name__)

    def __init__(self, actions, contained_words=None, exact_match=False):
        """
        Analyzer that searches the full cert domain names (subdomain.domain.tld) for the given words
        :param actions: A single action or a list of actions to be executed on every update
        :param contained_words: Words to search within the full domain
        :param exact_match: If set to True this analyzer will only match if the domain matches exactly any of the given words
        """
        super().__init__(actions)
        # Remove empty words
        self.contained_words = [word for word in listify(contained_words) if word != ""]
        self.exact_match = exact_match

    def match(self, update):
        matches = []

        if update is None or update.all_domains is None:
            self.logger.warning("Update is None!")
            return matches

        for word in self.contained_words:
            for full_domain in update.all_domains:
                if self.exact_match:
                    # If we only want exact matches, we check on equality
                    if word == full_domain:
                        matches.append(full_domain)
                else:
                    # If we want partial matches as well, we check if it contains the word
                    if word in full_domain:
                        matches.append(full_domain)

        return list(set(matches))
