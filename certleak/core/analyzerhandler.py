
import logging
from queue import Empty, Queue
from threading import Event, Lock
from time import sleep

from certleak.util import join_threads, start_thread


class AnalyzerHandler(object):
    """The AnalyzerHandler dispatches certificate updates to the analyzers"""

    def __init__(self, update_queue, action_queue=None, exception_event=None):
        self.logger = logging.getLogger(__name__)
        self.update_queue = update_queue
        self.action_queue = action_queue or Queue()
        self.analyzers = []
        self.running = False

        self.__lock = Lock()
        self.__threads = []
        self.__thread_pool = set()
        self.__exception_event = exception_event or Event()
        self.__stop_event = Event()

    def _pool_thread(self):
        while True:
            pass

    def add_analyzer(self, analyzer):
        """Adds an analyzer to the list of analyzers"""
        with self.__lock:
            if analyzer not in self.analyzers:
                self.analyzers.append(analyzer)

    def start(self, workers=4, ready=None):
        """Starts dispatching the certificate updates to the list of analyzers"""
        with self.__lock:
            if not self.running:
                if len(self.analyzers) == 0:
                    self.logger.warning("No analyzers added! At least one analyzer must be added prior to use!")
                    return None

                self.running = True
                thread = start_thread(self._start_analyzing, "AnalyzerHandler", exception_event=self.__exception_event)
                self.__threads.append(thread)

            if ready is not None:
                ready.set()

            return self.action_queue

    def _start_analyzing(self):
        while self.running:
            try:
                # Get cert update from queue
                update = self.update_queue.get(block=True, timeout=1)

                # TODO implement thread pool to limit number of parallel executed threads
                # Don't add these threads to the list. Otherwise they will just block the list
                start_thread(self._process_update, "process_update", update=update, exception_event=self.__exception_event)
            except Empty:
                if self.__stop_event.is_set():
                    self.logger.debug("orderly stopping")
                    self.running = False
                    break
                elif self.__exception_event.is_set():
                    self.logger.critical("stopping due to exception in another thread")
                    self.running = False
                    break
                continue

    def _process_update(self, update):
        if update is None:
            logging.warning("Update is None, skipping!")

        self.logger.debug(f"Analyzing update: {update.all_domains}")
        for analyzer in self.analyzers:
            matches = analyzer.match(update)

            if matches:
                # If the analyzer just returns a boolean, we pass an empty list
                if isinstance(matches, bool):
                    # matches == True, hence we pass an empty list
                    matches = []
                elif not isinstance(matches, list):
                    # when matches is not a bool, we pass the object as list
                    matches = [matches]
                actions = analyzer.actions
                self.action_queue.put((actions, update, analyzer, matches))

    def stop(self):
        """Stops dispatching updates to the analyzers"""
        self.logger.info("Orderly stopping AnalyzerHandler!")
        self.__stop_event.set()
        while self.running:
            sleep(0.1)
        self.__stop_event.clear()

        join_threads(self.__threads)
        self.__threads = []
