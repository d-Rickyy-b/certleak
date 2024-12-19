import logging
import time
from threading import Lock, Event

from certstream.core import CertStreamClient

from certleak.core.certstreamdata.message import Message
from certleak.util import start_thread, join_threads


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

        # Statistics
        self.last_info = 0
        self.update_counter = 0
        self.error_counter = 0
        self.processed_domains = set()

    def _handle_message(self, message, context):
        try:
            self._fill_queue(message, context)
        except Exception as e:
            logging.error("Exception while handling certstream message!", e)

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

        self.update_counter += 1
        try:
            msg = Message.from_dict(message)
            update = msg.update
        except Exception as e:
            self.logger.error("Something went wrong while de_jsoning: " + str(e))
            self.error_counter += 1
            return
        else:
            self.update_queue.put(update)

        if msg.update and msg.update.all_domains:
            for domain in msg.update.all_domains:
                self.processed_domains.add(domain)

        time_passed = int(time.time()) - self.last_info
        if time_passed >= 60:
            format_str = "Processed {0} updates ({1} unique domains) during the last {2} seconds. {3:.1f} domains/s, {4:.1f} certs/s"
            formatted_str = format_str.format(self.update_counter,
                                              len(self.processed_domains), time_passed,
                                              len(self.processed_domains) / time_passed, self.update_counter / time_passed)
            self.logger.info(formatted_str)

            format_str = "Queue length: {0}"
            self.logger.info(format_str.format(self.update_queue.qsize()))

            self.update_counter = 0
            self.error_counter = 0
            self.last_info = int(time.time())
            self.processed_domains = set()

    def _on_error(self, ex):
        """
        Error handler for the certstream module
        :return:
        """
        self.logger.error("An error occurred: {0}".format(ex))

    def _on_close(self, ex):
        """
        Error handler for the certstream module
        :return:
        """
        self.logger.error("An error occurred: ex: {0}".format(ex))

    def _run(self):
        """
        Internal method that starts the CertStreamClient and continouusly downloads cert updates as long as neither the stop nor exception event are set
        :return:
        """
        while not self.__stop_event.is_set() and not self.__exception_event.is_set():
            self.certstream_client = CertStreamClient(self._handle_message, self.certstream_url, skip_heartbeats=True)
            self.certstream_client._on_error = self._on_error
            self.certstream_client._on_close = self._on_close
            self.certstream_client.run_forever(ping_interval=30)
            time.sleep(1)

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
