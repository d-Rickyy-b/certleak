# -*- coding: utf-8 -*-
import logging

from .basicaction import BasicAction


class LogAction(BasicAction):
    """Action to log a cert update to console"""
    name = "LogAction"

    def __init__(self, level):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.level = level

    def perform(self, update, analyzer_name=None, matches=None):
        #TODO implement templating, that way we could specify what exactly should get printed
        self.logger.log(self.level, "New certificate update matched: {0}\n".format(update))
