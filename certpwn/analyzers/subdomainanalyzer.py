# -*- coding: utf-8 -*-
import logging

import tldextract

from certpwn.util import listify
from .basicanalyzer import BasicAnalyzer


class SubDomainAnalyzer(BasicAnalyzer):
    """Analyzer to match subdomains containing certain strings"""
    name = "SubDomainAnalyzer"
    logger = logging.getLogger(__name__)

    def __init__(self, actions, subdomains, exact_match=True):
        """
        Analyzer that searches the full cert domain names (subdomain.domain.tld) for the given words
        :param actions: A single action or a list of actions to be executed on every update
        :param subdomains: The subdomains to search for
        :param exact_match: If set to True (default) it will only search for exact subdomain matches, else it will allow for partly matches
        """
        super().__init__(actions)
        self.subdomains = listify(subdomains)
        self.exact_match = exact_match

    def match(self, update):
        matches = []

        if update is None or update.all_domains is None:
            self.logger.warning("Update is None!")
            return matches

        for domain in update.all_domains:
            extracted = tldextract.extract(domain)
            subdomains_full = extracted.subdomain
            subdomains = subdomains_full.split(".")

            for subdomain in subdomains:
                if self.exact_match:
                    if subdomain in self.subdomains:
                        matches.append(domain)
                        continue

        return list(set(matches))
