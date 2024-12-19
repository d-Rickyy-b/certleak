from .basicaction import BasicAction


class DatabaseAction(BasicAction):
    """Action to save a cert update to a database."""

    name = "DatabaseAction"

    def __init__(self, database):
        super().__init__()
        self.database = database

    def perform(self, update, analyzer_name=None, matches=None):
        """Store an incoming cert update in the database."""
        self.database.store(update)
