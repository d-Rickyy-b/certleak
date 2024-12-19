class CertleakError(Exception):
    """Representation of a certleak error object."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the error message as a string."""
        return str(self.message)


class InvalidActionError(CertleakError):
    """Representation of an error for invalid actions passed to analyzers."""

    pass
