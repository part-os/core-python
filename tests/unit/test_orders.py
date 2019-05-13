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

    def test_date_fmt(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        self.assertEqual(2019, oi.ships_on_dt.year)
        self.assertEqual(5, oi.ships_on_dt.month)
        self.assertEqual(22, oi.ships_on_dt.day)
        self.assertEqual(2019, o.created_dt.year)
        self.assertEqual(5, o.created_dt.month)
        self.assertEqual(8, o.created_dt.day)

    def test_operation_mapper(self):
        op1 = {
            'name': 'name1',
            'notes': None,
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
            'notes': None,
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
            'notes': 'A note',
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
        self.assertEqual('A note', op.notes)

    def test_ship_desc(self):
        from paperless.objects.orders import ShippingOption
        import datetime
        dt = datetime.datetime.now()

        # pickup
        so1 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            ship_when='all_at_once',
            shipping_method=None,
            type='pickup'
        )
        self.assertTrue(so1.summary(dt, '').startswith(
            'Customer will pickup from supplier\'s location.',))

        # customer's account
        so2 = ShippingOption(
            customers_account_number='12345',
            customers_carrier='ups',
            ship_when='all_at_once',
            shipping_method='ground',
            type='customers_shipping_account'
        )
        self.assertIn('Use Customer\'s Shipping Account', so2.summary(dt, ''))
        self.assertIn('Method: GROUND', so2.summary(dt, ''))

        # supplier's account
        so3 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            ship_when='all_at_once',
            shipping_method='ground',
            type='suppliers_shipping_account'
        )
        summ = so3.summary(dt, 'credit_card')
        self.assertIn('has been charged', summ)
        summ = so3.summary(dt, 'purchase_order')
        self.assertIn('bill customer', summ)
