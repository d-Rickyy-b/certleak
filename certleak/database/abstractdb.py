class AbstractDB:
    def __init__(self):
        pass

    def store(self, update):
        """Store a cert update in the database."""
        raise NotImplementedError
