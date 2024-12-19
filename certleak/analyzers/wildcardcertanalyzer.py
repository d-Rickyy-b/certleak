
import tldextract

from certleak.util import listify

from .basicanalyzer import BasicAnalyzer


class WildcardCertAnalyzer(BasicAnalyzer):
    """
    Analyzer for finding wildcard certificates
    """

    name = "WildcardCertAnalyzer"

    def __init__(self, actions, blacklist=None):
        super().__init__(actions)
        self.blacklist = listify(blacklist)

    def match(self, update):
        """
        Matches if at least one of the subdomains of this certificate is '*', which is a wildcard domain
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
            except Exception as e:
                self.logger.error("During matching of an update, the following exception occurred: {0}".format(e))
                continue

            if extract_result.subdomain == "*" and not any(word in full_domain for word in self.blacklist):
                matches.append(full_domain)

        return list(set(matches))
