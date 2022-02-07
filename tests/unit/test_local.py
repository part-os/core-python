import os
import time
import unittest

from paperless.local import DEFAULT_IMPLEMENTATION, LocalStorage
from paperless.objects.orders import Order
from paperless.objects.quotes import QuoteOperation


class TestLocalStorage(unittest.TestCase):
    def test_factory(self):
        self.assertIsInstance(
            LocalStorage.get_instance('/tmp/test'), DEFAULT_IMPLEMENTATION
        )

    def test_local(self):
        filename = '/tmp/test'
        if os.path.exists(filename):
            os.remove(filename)
        storage = LocalStorage.get_instance(filename)
        self.assertIsNone(storage.get_last_processed(Order))
        storage.process(Order, 1, True)
        self.assertEqual(1, storage.get_last_processed(Order))
        # last processed is by timestamp, so they need to be 1 sec apart
        time.sleep(1.1)
        storage.process(Order, 2, True)
        self.assertEqual(2, storage.get_last_processed(Order))
        storage.process(QuoteOperation, 10, True)
        storage.clear_cache(Order)
        self.assertIsNone(storage.get_last_processed(Order))
        self.assertEqual(10, storage.get_last_processed(QuoteOperation))
        storage.clear_cache()
        self.assertIsNone(storage.get_last_processed(QuoteOperation))
        os.remove(filename)
