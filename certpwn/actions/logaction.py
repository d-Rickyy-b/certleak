# -*- coding: utf-8 -*-
import logging

from certpwn.util import TemplatingEngine
from .basicaction import BasicAction


class LogAction(BasicAction):
    """Action to log a cert update to console"""
    name = "LogAction"

    def __init__(self, level, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.level = level
        self.template = template

    def perform(self, update, analyzer_name=None, matches=None):
        text = TemplatingEngine.fill_template(update, analyzer_name, template_string=self.template, matches=matches)
        self.logger.log(self.level, text)
