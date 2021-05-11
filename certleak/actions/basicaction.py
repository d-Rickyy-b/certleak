# -*- coding: utf-8 -*-
import logging


class BasicAction(object):
    """Base class for actions which can be performed on updates"""
    name = "BasicAction"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def perform(self, update, analyzer_name=None, matches=None):
        """Perform the action on the passed update"""
        raise NotImplementedError
