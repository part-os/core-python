import unittest
import json
from decimal import Decimal
from unittest.mock import MagicMock

from paperless.objects.orders import Order
from paperless.client import PaperlessClient


class TestOrders(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/order.json') as data_file:
            self.mock_order_json = json.load(data_file)

    def test_get_order(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        self.assertEqual(o.number, 16)
        self.assertEqual('credit_card', o.payment_details.payment_type)
        self.assertEqual('pending', o.status)
        self.assertEqual(73, o.quote_number)
        self.assertEqual(len(o.order_items), 3)
        # test assembly order item
        assmb_oi = o.order_items[0]
        self.assertEqual(assmb_oi.id, 17135)
        self.assertEqual(len(assmb_oi.components), 8)
        self.assertEqual((assmb_oi.quote_item_id), 27122)
        # test single component order item
        standard_oi = o.order_items[1]
        self.assertEqual(standard_oi.id, 17136)
        self.assertEqual(standard_oi.root_component_id, 30880)
        self.assertEqual(len(standard_oi.components), 1)
        self.assertIsNone(standard_oi.add_on_fees)
        root_component = standard_oi.components[0]
        self.assertEqual(len(root_component.material_operations), 2)
        self.assertEqual(len(root_component.shop_operations), 7)
        finish_op = root_component.shop_operations[6]
        self.assertEqual(finish_op.name, 'Chromate')
        self.assertEqual(finish_op.cost.dollars, 150.)
        self.assertIsNone(finish_op.setup_time)
        self.assertIsNone(finish_op.get_variable('bad name'))
        # test add ons
        other_oi = o.order_items[0]
        self.assertEqual(other_oi.base_price.dollars, Decimal('3086.88'))
        add_on = other_oi.ordered_add_ons[0]
        self.assertEqual(add_on.quantity, 1)
        # test manual line item
        manual_oi = o.order_items[2]
        self.assertEqual('manual', manual_oi.quote_item_type)
        self.assertEqual('', manual_oi.description)

    def test_date_fmt(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        self.assertEqual(2020, oi.ships_on_dt.year)
        self.assertEqual(2, oi.ships_on_dt.month)
        self.assertEqual(7, oi.ships_on_dt.day)
        self.assertEqual(2020, o.created_dt.year)
        self.assertEqual(1, o.created_dt.month)
        self.assertEqual(21, o.created_dt.day)

    def test_ship_desc(self):
        from paperless.objects.orders import ShippingOption
        import datetime
        dt = datetime.datetime.now()

        # pickup
        so1 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            shipping_method=None,
            type='pickup'
        )
        self.assertTrue(so1.summary(dt, '').startswith(
            'Customer will pickup from supplier\'s location.',))

        # customer's account
        so2 = ShippingOption(
            customers_account_number='12345',
            customers_carrier='ups',
            shipping_method='ground',
            type='customers_shipping_account'
        )
        self.assertIn('Use Customer\'s Shipping Account', so2.summary(dt, ''))
        self.assertIn('Method: GROUND', so2.summary(dt, ''))

        # supplier's account
        so3 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            shipping_method='ground',
            type='suppliers_shipping_account'
        )
        summ = so3.summary(dt, 'credit_card')
        self.assertIn('has been charged', summ)
        summ = so3.summary(dt, 'purchase_order')
        self.assertIn('bill customer', summ)
