import time
from .listeners import BaseListener

class PaperlessSDK:
    listeners = []
    #delay = 30
    delay = 3

    #todo add a type for a base listener
    def add_listener(self, listener: BaseListener):
        #todo: assert it is a listener
        #todo: should we verify that we only listen to one of each types of listeners? Will we run into any situations with threading where we detect (or don't detect) multiple of the same objects?
        self.listeners.append(listener)

    def run(self):
        while True:
            for listener in self.listeners:
                listener.listen()
            time.sleep(self.delay)


