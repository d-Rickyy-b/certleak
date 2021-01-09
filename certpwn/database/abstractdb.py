# -*- coding: utf-8 -*-


class AbstractDB(object):

    def __init__(self):
        pass

    def store(self, update):
        """Stores a cert update in the database"""
        raise NotImplementedError
