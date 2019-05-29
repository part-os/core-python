import time
import logging
from .listeners import BaseListener

LOGGER = logging.getLogger(__name__)


class PaperlessSDK:
    listeners = []
    delay = 60 * 15  # 15 minutes

    def add_listener(self, listener: BaseListener):
        assert(isinstance(listener, BaseListener))
        self.listeners.append(listener)

    def run(self):
        while True:
            for listener in self.listeners:
                try:
                    listener.listen()
                except Exception as e:
                    LOGGER.exception('Unhandled exception in listener')
            time.sleep(self.delay)
