# -*- coding: utf-8 -*-
import logging
from certpwn.util import listify
from .basicanalyzer import BasicAnalyzer


class FullDomainAnalyzer(BasicAnalyzer):
    """Analyzer to match domains containing certain strings"""
    name = "FullDomainAnalyzer"
    logger = logging.getLogger(__name__)

    def __init__(self, actions, contained_words=None):
        """
        Analyzer that searches the full cert domain names (subdomain.domain.tld) for the given words
        :param actions:
        :param contained_words:
        """
        super().__init__(actions)
        # Remove empty words
        self.contained_words = [word for word in listify(contained_words) if word != ""]

    def match(self, update):
        matches = []

        if update is None or update.all_domains is None:
            self.logger.warning("Update is None!")
            return matches

        for word in self.contained_words:
            for full_domain in update.all_domains:
                if word in full_domain:
                    matches.append(full_domain)

        return list(set(matches))
