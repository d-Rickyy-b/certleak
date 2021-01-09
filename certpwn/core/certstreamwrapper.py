# -*- coding: utf-8 -*-
import logging
import time
from threading import Lock, Event

from certstream.core import CertStreamClient

from certpwn.core import Message
from certpwn.util import start_thread, join_threads


class CertstreamWrapper(object):

    def __init__(self, update_queue, certstream_url, exception_event):
        """
        The CertstreamWrapper is a wrapper around the python certstream module, allowing it to run in its own thread and filling new cert updates into a queue.
        :param update_queue: The queue into which new updates are sent
        :param certstream_url: The websocket URL from which certstream fetches new cert updates
        :param exception_event: An event that gets set when an unexpected exception occurs. Causes the thread to halt if set
        """
        self.logger = logging.getLogger(__name__)
        self.update_queue = update_queue
        self.certstream_url = certstream_url
        self.certstream_client = None
        self.__exception_event = exception_event or Event()
        self.__stop_event = Event()
        self.__lock = Lock()
        self.__threads = []
        self.running = False

    def _fill_queue(self, message, context):
        """
        This method is being used as a callback function for the certstream module. It get's called on each new message.
        :param message: dict
        :param context: context
        :return:
        """
        if message["message_type"] == "heartbeat":
            self.logger.debug("New heartbeat received!")
            return

        try:
            msg = Message.from_dict(message)
            self.update_queue.put(msg.update)
        except Exception as e:
            self.logger.error("Something went wrong while de_jsoning: " + str(e))

    def _on_error(self, ex):
        """
        Error handler for the certstream module
        :return:
        """
        return

    def _run(self):
        """
        Internal method that starts the CertStreamClient and continouusly downloads cert updates as long as neither the stop nor exception event are set
        :return:
        """
        while not self.__stop_event.is_set() and not self.__exception_event.is_set():
            self.certstream_client = CertStreamClient(self._fill_queue, self.certstream_url)
            self.certstream_client._on_error = self._on_error
            self.certstream_client.run_forever(ping_interval=15)
            time.sleep(5)

    def start(self):
        """
        Start certstream in own thread
        :return:
        """
        with self.__lock:
            if not self.running:
                self.running = True
                thread = start_thread(self._run, "CertstreamWrapper", exception_event=self.__exception_event)
                self.__threads.append(thread)

    def stop(self):
        """Stops dispatching updates to the analyzers"""
        self.logger.info("Orderly stopping CertstreamWrapper!")
        with self.__lock:
            self.__stop_event.set()
            self.certstream_client.close()
            join_threads(self.__threads)
            self.__threads = []
            self.running = False
            self.__stop_event.clear()
