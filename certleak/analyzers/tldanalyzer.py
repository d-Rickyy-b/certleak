import tldextract

from certleak.util import listify

from .basicanalyzer import BasicAnalyzer


class TLDAnalyzer(BasicAnalyzer):
    """Analyzer to check for certain TLDs"""

    name = "TLDAnalyzer"

    def __init__(self, actions, filtered_tlds, blacklist=None):
        super().__init__(actions)
        self.filtered_tlds = listify(filtered_tlds)
        self.blacklist = listify(blacklist)

    def match(self, update):
        """
        Matches if the TLD of any domain contains any of the passed TLDs
        :param update: The certificate Update object
        :return:
        """
        matches = []
        if update is None or update.all_domains is None:
            self.logger.warning("Update is None!")
            return matches

        for full_domain in update.all_domains:
            try:
                extract_result = tldextract.extract(full_domain)

                for tld in self.filtered_tlds:
                    if extract_result.suffix == tld and not any(word in full_domain for word in self.blacklist):
                        matches.append(full_domain)
            except Exception as e:
                self.logger.error(f"During matching of an update, the following exception occurred: {e}")

        return set(matches)
