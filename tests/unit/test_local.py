import unittest
import os
from paperless.local import LocalStorage, DEFAULT_IMPLEMENTATION
from paperless.objects.orders import Order, Operation


class TestLocalStorage(unittest.TestCase):
    def test_factory(self):
        self.assertIsInstance(LocalStorage.get_instance('/tmp/test'),
                              DEFAULT_IMPLEMENTATION)

    def test_local(self):
        filename = '/tmp/test'
        if os.path.exists(filename):
            os.remove(filename)
        storage = LocalStorage.get_instance(filename)
        self.assertIsNone(storage.get_last_processed(Order))
        storage.process(Order, 1, True)
        self.assertEqual(1, storage.get_last_processed(Order))
        storage.process(Order, 2, True)
        self.assertEqual(2, storage.get_last_processed(Order))
        storage.process(Operation, 10, True)
        storage.clear_cache(Order)
        self.assertIsNone(storage.get_last_processed(Order))
        self.assertEqual(10, storage.get_last_processed(Operation))
        storage.clear_cache()
        self.assertIsNone(storage.get_last_processed(Operation))
        os.remove(filename)
