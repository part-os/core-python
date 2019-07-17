import unittest
import os
from unittest.mock import Mock, MagicMock
from paperless.listeners import BaseListener, OrderListener
from paperless.objects.orders import Order
from paperless.exceptions import PaperlessNotFoundException


def mock_get(order_id):
    if order_id == 3:
        order = Mock()
        order.number = 3
        return order
    else:
        raise PaperlessNotFoundException('')


class TestListener(unittest.TestCase):
    class MyOrderListener(OrderListener):
        def on_event(self, resource):
            return True

    @unittest.mock.patch('paperless.objects.orders.Order.get', side_effect=mock_get)
    def test_listener(self, _):
        filename = '/tmp/test'
        if os.path.exists(filename):
            os.remove(filename)
        listener = self.MyOrderListener(filename)

        listener.local_storage.process(Order, 2, True)

        order = Mock()
        order.number = 2
        Order.list = MagicMock(return_value=[order])
        self.assertEqual(2, listener.get_default_last_record_id())

        listener.listen()
        self.assertEqual(3, listener.local_storage.get_last_processed(Order))
        listener.listen()
        self.assertEqual(3, listener.local_storage.get_last_processed(Order))
