import unittest
from unittest.mock import Mock, MagicMock
from paperless.listeners import BaseListener, OrderListener
from paperless.objects.orders import Order


class TestListener(unittest.TestCase):
    class MyOrderListener(OrderListener):
        def on_event(self, resource):
            return True

    def test_listener(self):
        filename = '/tmp/test'
        listener = self.MyOrderListener(filename)
        listener.get_new_resource = MagicMock(return_value=None)
        order = Mock()
        order.number = 3
        Order.list = MagicMock(return_value=[order])
        self.assertIsNone(listener.local_storage.get_last_processed(Order))
        self.assertEqual(3, listener.get_default_last_record_id())
        listener.listen()
        self.assertIsNone(listener.local_storage.get_last_processed(Order))
        order = Mock()
        order.number = 4
        listener.get_new_resource = MagicMock(return_value=order)
        listener.listen()
        self.assertEqual(4, listener.local_storage.get_last_processed(Order))
