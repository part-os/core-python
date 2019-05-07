#TODO: TEST ORDER LIST

import unittest
import json
from unittest.mock import MagicMock

from paperless.objects.orders import Order
from paperless.client import PaperlessClient

class TestOrders(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient(
            username="test",
            password="test"
        )
        with open('tests/unit/mock_data/order.json') as data_file:
            self.mock_order_json = json.load(data_file)

    def test_get_order(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        self.assertEqual(o.number, 31) # 31 is loaded from mock order json

