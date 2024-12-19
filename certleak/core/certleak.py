import logging
from queue import Queue
from signal import SIGABRT, SIGINT, SIGTERM, signal
from threading import Event
from time import sleep

from certleak.core.actionhandler import ActionHandler
from certleak.core.analyzerhandler import AnalyzerHandler
from certleak.core.certstreamwrapper import CertstreamWrapper


class CertLeak:
    def __init__(self, certstream_url="wss://certstream.calidog.io/"):
        """
        Basic CertLeak object, handling the connection to the certstream network and all the analyzers and actions
        :param certstream_url: The websocket URL from which certstream fetches new cert updates
        """
        self.logger = logging.getLogger(__name__)
        self.is_idle = True
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
        Start CertLeak
        :return:
        """
        self.logger.info("Starting certleak!")
        self.certstream_wrapper.start()
        self.analyzer_handler.start()
        self.action_handler.start()
        # Run until signal is received
        self.idle()

    def stop(self):
        """
        Stop CertLeak
        :return:
        """
        self.logger.info("Orderly stopping certleak!")
        self.certstream_wrapper.stop()
        self.analyzer_handler.stop()
        self.action_handler.stop()

    def signal_handler(self, signum, frame):
        """Handler method to handle signals"""
        self.is_idle = False
        self.logger.info("Received signal %s, stopping...", signum)
        self.stop()

    def add_analyzer(self, analyzer):
        """
        Adds a new analyzer to the list of analyzers
        :param analyzer: Instance of a BasicAnalyzer
        :return: None
        """
        self.analyzer_handler.add_analyzer(analyzer)

    def idle(self, stop_signals=(SIGINT, SIGTERM, SIGABRT)):
        """
        Blocks until one of the signals are received and stops the updater.
        Thanks to the python-telegram-bot developers - https://github.com/python-telegram-bot/python-telegram-bot/blob/2cde878d1e5e0bb552aaf41d5ab5df695ec4addb/telegram/ext/updater.py#L514-L529
        :param stop_signals: The signals to which the code reacts to
        """
        self.is_idle = True

        for sig in stop_signals:
            signal(sig, self.signal_handler)

        while self.is_idle:
            if self.exception_event.is_set():
                self.logger.warning("An exception occurred. Calling exception handlers and going down!")

                self.is_idle = False
                self.stop()
                return

            sleep(1)
