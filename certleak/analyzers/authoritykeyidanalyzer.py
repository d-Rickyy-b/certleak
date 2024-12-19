
from .basicanalyzer import BasicAnalyzer


class AuthorityKeyIDAnalyzer(BasicAnalyzer):
    """Analyzer for finding certificate updates that are signed by a CA with a specified subject key identifier"""

    name = "AuthorityKeyIDAnalyzer"

    def __init__(self, actions, authority_key_id):
        """
        Find a CA with a specific authority_key_id
        :param actions:
        :param authority_key_id: Certificate authorityKeyID, string separated by colons
        """
        super().__init__(actions)

        authority_key_id = authority_key_id.replace("keyid:", "")
        authority_key_id = authority_key_id.replace(r"\n", "")
        self.authority_key_id = authority_key_id.lower()

    def match(self, update):
        if not update:
            return False

        authority_key_identifier = update.extensions.authorityKeyIdentifier
        if authority_key_identifier is None:
            return False

        authority_key_identifier = authority_key_identifier.replace("keyid:", "")
        authority_key_identifier.replace(r"\n", "")

        return authority_key_identifier.lower() == self.authority_key_id
