import unittest
import json
from decimal import Decimal
from unittest.mock import MagicMock

from paperless.objects.components import ChildComponent
from paperless.objects.orders import Order, OrderComponent
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
        self.assertEqual(o.number, 43)
        self.assertEqual('credit_card', o.payment_details.payment_type)
        self.assertEqual('confirmed', o.status)
        self.assertEqual(139, o.quote_number)
        self.assertEqual(len(o.order_items), 3)
        # test assembly order item
        assmb_oi = o.order_items[0]
        self.assertEqual(len(assmb_oi.components), 8)
        assmb_root_component = assmb_oi.root_component
        self.assertEqual(len(assmb_root_component.child_ids), 3)
        self.assertEqual(assmb_root_component.deliver_quantity, 5)
        self.assertIsNone(assmb_root_component.description)
        self.assertFalse(assmb_root_component.export_controlled)
        self.assertEqual(assmb_root_component.finishes, ['Chromate'])
        self.assertEqual(assmb_root_component.innate_quantity, 1)
        self.assertTrue(assmb_root_component.is_root_component)
        self.assertEqual(assmb_root_component.make_quantity, 5)
        self.assertEqual(assmb_root_component.material.family, 'Aluminum')
        self.assertEqual(len(assmb_root_component.material_operations), 0)
        self.assertEqual(len(assmb_root_component.parent_ids), 0)
        self.assertEqual(assmb_root_component.part_name, 'small-sub-assembly.STEP')
        self.assertIsNone(assmb_root_component.part_number)
        self.assertEqual(assmb_root_component.part_uuid, 'ddab27ae-ff7b-4db2-be24-41002be6cb58')
        self.assertEqual(assmb_root_component.process.name, 'CNC Machining')
        self.assertIsNone(assmb_root_component.revision)
        self.assertEqual(len(assmb_root_component.shop_operations), 1)
        self.assertEqual(len(assmb_root_component.supporting_files), 1)
        self.assertEqual(assmb_root_component.type, 'assembled')
        # test single component order item
        standard_oi = o.order_items[1]
        self.assertEqual(len(standard_oi.components), 1)
        self.assertIsNone(standard_oi.add_on_fees)
        root_component = standard_oi.root_component
        self.assertEqual(len(root_component.material_operations), 2)
        self.assertEqual(len(root_component.shop_operations), 7)
        finish_op = root_component.shop_operations[6]
        self.assertEqual(finish_op.name, 'Chromate')
        self.assertEqual(finish_op.cost.dollars, 150.)
        self.assertIsNone(finish_op.setup_time)
        self.assertIsNone(finish_op.get_variable('bad name'))
        op_quantity = finish_op.quantities[0]
        self.assertEqual(op_quantity.quantity, 25)
        # test add ons
        other_oi = o.order_items[0]
        self.assertEqual(other_oi.base_price.dollars, Decimal('2757.80'))
        add_on = other_oi.ordered_add_ons[0]
        self.assertEqual(add_on.quantity, 5)
        # test manual line item
        manual_oi = o.order_items[2]
        self.assertEqual('manual', manual_oi.quote_item_type)
        self.assertEqual('', manual_oi.description)

    def test_date_fmt(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        self.assertEqual(2020, oi.ships_on_dt.year)
        self.assertEqual(4, oi.ships_on_dt.month)
        self.assertEqual(21, oi.ships_on_dt.day)
        self.assertEqual(2020, o.created_dt.year)
        self.assertEqual(4, o.created_dt.month)
        self.assertEqual(2, o.created_dt.day)

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

    def test_assemblies(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        assm = list(oi.iterate_assembly())
        self.assertEqual(8, len(assm))
        self.assertTrue(assm[0].component.is_root_component)
        self.assertEqual(0, assm[0].level)
        expected_order = [
            49809, 49815, 49814, 49816, 49813, 49812, 49811, 49810]
        self.assertEqual(
            expected_order,
            [c.component.id for c in assm]
        )
        self.assertEqual(2, assm[4].level)
        self.assertEqual(4, assm[4].level_count)

    def test_hardware(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        found_hardware = False
        total_q = 0
        oc: OrderComponent
        for oc in oi.components:
            if oc.part_number == 'AC-M6-2':
                self.assertTrue(oc.is_hardware)
                found_hardware = True
                for parent_id in oc.parent_ids:
                    parent = oi.get_component(parent_id)
                    self.assertEqual('assembled', parent.type)
                    child: ChildComponent
                    for child in parent.children:
                        if child.child_id == oc.id:
                            total_q += child.quantity
            else:
                self.assertFalse(oc.is_hardware)
        self.assertTrue(found_hardware)
        self.assertEqual(1, total_q)
