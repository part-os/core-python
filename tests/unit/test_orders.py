#TODO: TEST ORDER LIST

import unittest
import json
from unittest.mock import MagicMock

from paperless.objects.orders import Order, Operation
from paperless.client import PaperlessClient
from paperless.api_mappers import OperationMapper


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
        self.assertEqual(o.number, 192)
        op1 = o.order_items[0].operations[3]
        self.assertEqual(2, op1.setup_time)
        self.assertEqual('Net 30', o.payment_details.terms)

    def test_operation_mapper(self):
        op1 = {
            'name': 'name1',
            'display_context': [
                {"primary_key": "variables", "secondary_key": "runtime",
                 "value": 1.0, "type": "number"},
                {"primary_key": "variables", "secondary_key": "other",
                 "value": 1.0, "type": "number"}
            ],
        }
        op: Operation = Operation(**OperationMapper.map(op1))
        self.assertEqual('name1', op.name)
        self.assertEqual(1.0, op.runtime)
        self.assertIsNone(op.setup_time)

        op2 = {
            'name': 'name1',
            'display_context': [
                {"primary_key": "variables", "secondary_key": "runtime",
                 "value": 1.0, "type": "number"},
                {"primary_key": "variables", "secondary_key": "setup_time",
                 "value": 2.0, "type": "number"}
            ],
            'overrides': {}
        }
        op: Operation = Operation(**OperationMapper.map(op2))
        self.assertEqual(1.0, op.runtime)
        self.assertEqual(2.0, op.setup_time)

        op3 = {
            'name': 'name1',
            'display_context': [
                {"primary_key": "variables", "secondary_key": "runtime",
                 "value": 1.0, "type": "number"},
                {"primary_key": "variables", "secondary_key": "setup_time",
                 "value": 2.0, "type": "number"}
            ],
            'overrides': {'variables': {'runtime': '0.25'}}
        }
        op: Operation = Operation(**OperationMapper.map(op3))
        self.assertEqual(0.25, op.runtime)
        self.assertEqual(2.0, op.setup_time)
