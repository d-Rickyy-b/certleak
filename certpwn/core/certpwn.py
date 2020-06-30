# -*- coding: utf-8 -*-
import logging
from queue import Queue
from threading import Event

from certpwn.core import ActionHandler, AnalyzerHandler, CertstreamWrapper


class CertPwn(object):

    def __init__(self, certstream_url="wss://certstream.calidog.io/"):
        """
        Basic CertPwn object, handling the connection to the certstream network and all the analyzers and actions
        :param certstream_url: The websocket URL from which certstream fetches new cert updates
        """
        self.logger = logging.getLogger(__name__)
        self.update_queue = Queue()
        self.action_queue = Queue()
        self.exception_event = Event()
        self.certstream_url = certstream_url
        self.c = None

        self.analyzer_handler = AnalyzerHandler(update_queue=self.update_queue, action_queue=self.action_queue, exception_event=self.exception_event)
        self.action_handler = ActionHandler(action_queue=self.action_queue, exception_event=self.exception_event)
        self.certstream_wrapper = CertstreamWrapper(update_queue=self.update_queue, certstream_url=certstream_url, exception_event=self.exception_event)

    def start(self):
        """
        Start CertPwn
        :return:
        """
        self.logger.info("Starting certpwn!")
        self.certstream_wrapper.start()
        self.analyzer_handler.start()
        self.action_handler.start()

    def stop(self):
        """
        Stop CertPwn
        :return:
        """
        self.logger.info("Orderly stopping certpwn!")
        self.certstream_wrapper.stop()
        self.analyzer_handler.stop()
        self.action_handler.stop()

    def add_analyzer(self, analyzer):
        """
        Adds a new analyzer to the list of analyzers
        :param analyzer: Instance of a BasicAnalyzer
        :return: None
        """
        self.analyzer_handler.add_analyzer(analyzer)
