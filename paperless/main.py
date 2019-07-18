import time
import logging
from .listeners import BaseListener

LOGGER = logging.getLogger(__name__)

DEFAULT_DELAY = 60 * 15  # 15 minutes
DEFAULT_LOOP = True


class PaperlessSDK:
    def __init__(self, delay=None, loop=None):
        """
        Initialize the SDK object

        :param delay: listen interval in seconds
        :param loop: if False, listeners runs a single time; otherwise, they
        loop forever
        """
        self.listeners = []
        if delay is not None:
            self.delay = delay
        else:
            self.delay = DEFAULT_DELAY
        if loop is not None:
            self.loop = loop
        else:
            self.loop = DEFAULT_LOOP

    def add_listener(self, listener: BaseListener):
        assert(isinstance(listener, BaseListener))
        self.listeners.append(listener)

    def run(self):
        first_run = True
        while first_run or self.loop:
            if not first_run:
                time.sleep(self.delay)
            first_run = False
            for listener in self.listeners:
                try:
                    listener.listen()
                except Exception as e:
                    LOGGER.exception('Unhandled exception in listener')
