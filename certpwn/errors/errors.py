# -*- coding: utf-8 -*-


class CertpwnError(Exception):
    """Representation of a certpwn error object."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return '%s' % self.message


class InvalidActionError(CertpwnError):
    """Representation of an error for invalid actions passed to analyzers"""
    pass
