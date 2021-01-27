import json
import unittest
from decimal import Decimal
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.components import ChildComponent
from paperless.objects.orders import Order, OrderComponent


class TestOrders(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/order.json') as data_file:
            self.mock_order_json = json.load(data_file)

        with open('tests/unit/mock_data/minimal_order.json') as data_file:
            self.mock_minimal_order_json = json.load(data_file)

    def test_get_order(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        self.assertEqual(o.number, 179)
        self.assertEqual('credit_card', o.payment_details.payment_type)
        self.assertEqual('pending', o.status)
        self.assertEqual(339, o.quote_number)
        self.assertEqual(len(o.order_items), 3)
        # test salesperson
        sales_person = o.sales_person
        self.assertEqual(sales_person.first_name, 'Heathrow Chester')
        # test estimator
        estimator = o.estimator
        self.assertEqual(estimator.first_name, 'Heathrow Chester')
        # test assembly order item
        assmb_oi = o.order_items[0]
        self.assertEqual(len(assmb_oi.components), 8)
        assmb_root_component = assmb_oi.root_component
        self.assertEqual(len(assmb_root_component.child_ids), 3)
        self.assertEqual(assmb_root_component.deliver_quantity, 5)
        self.assertIsNone(assmb_root_component.description)
        self.assertFalse(assmb_root_component.export_controlled)
        self.assertEqual(assmb_root_component.finishes, [])
        self.assertEqual(assmb_root_component.innate_quantity, 1)
        self.assertTrue(assmb_root_component.is_root_component)
        self.assertEqual(assmb_root_component.make_quantity, 5)
        self.assertEqual(assmb_root_component.material.family, 'Aluminum')
        self.assertEqual(len(assmb_root_component.material_operations), 0)
        self.assertEqual(len(assmb_root_component.parent_ids), 0)
        self.assertEqual(assmb_root_component.part_name, 'small-sub-assembly.STEP')
        self.assertIsNone(assmb_root_component.part_number)
        self.assertEqual(
            assmb_root_component.part_uuid, 'ddab27ae-ff7b-4db2-be24-41002be6cb58'
        )
        self.assertEqual(assmb_root_component.process.name, 'CNC Machining')
        self.assertIsNone(assmb_root_component.revision)
        self.assertEqual(len(assmb_root_component.shop_operations), 1)
        self.assertEqual(len(assmb_root_component.supporting_files), 1)
        self.assertEqual(assmb_root_component.type, 'assembled')

        op = assmb_root_component.shop_operations[0]
        self.assertEqual('304-#4', op.get_variable('Material Selection'))
        self.assertEqual(150, op.get_variable('Lot Charge'))

        # test single component order item
        standard_oi = o.order_items[1]
        self.assertEqual(len(standard_oi.components), 1)
        self.assertEqual(standard_oi.add_on_fees.dollars, Decimal('50'))
        root_component = standard_oi.root_component
        self.assertEqual(len(root_component.material_operations), 2)
        self.assertEqual(len(root_component.shop_operations), 8)
        finish_op = root_component.shop_operations[6]
        self.assertEqual(finish_op.name, 'Chromate')
        self.assertEqual(finish_op.operation_definition_name, 'Chromate')
        self.assertEqual(finish_op.cost.dollars, 150.0)
        self.assertIsNone(finish_op.setup_time)
        self.assertIsNone(finish_op.get_variable('bad name'))

        # ensure quantities are in proper order
        op_quantities = [qty.quantity for qty in finish_op.quantities]
        self.assertEqual([1, 5, 10, 25], op_quantities)

        qty_specific_op = root_component.shop_operations[7]
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Num').value, 2)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Num').row, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Num').options, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').value, 'a')
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').row, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').options, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Drop Down Num').value, '2')
        self.assertEqual(qty_specific_op.get_variable_obj('Drop Down Num').row, None)
        self.assertEqual(
            qty_specific_op.get_variable_obj('Drop Down Num').options, ['1', '2', '3']
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').value, '6061-T6'
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').options, None
        )

        add_on = standard_oi.ordered_add_ons[0]
        self.assertEqual(add_on.get_variable('Basic Num').value, 2)
        self.assertEqual(add_on.get_variable('Basic Num').row, None)
        self.assertEqual(add_on.get_variable('Basic Num').options, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').value, 'a')
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').row, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Basic Str').options, None)
        self.assertEqual(qty_specific_op.get_variable_obj('Drop Down Num').value, '2')
        self.assertEqual(qty_specific_op.get_variable_obj('Drop Down Num').row, None)
        self.assertEqual(
            qty_specific_op.get_variable_obj('Drop Down Num').options, ['1', '2', '3']
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').value, '6061-T6'
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )
        self.assertEqual(
            qty_specific_op.get_variable_obj('Material Selection').options, None
        )

        # test add ons
        other_oi = o.order_items[0]
        self.assertEqual(other_oi.base_price.dollars, Decimal('2757.80'))
        add_on = other_oi.ordered_add_ons[0]
        self.assertEqual(add_on.quantity, 5)
        # test manual line item
        manual_oi = o.order_items[2]
        self.assertEqual('automatic', manual_oi.quote_item_type)
        self.assertEqual('', manual_oi.description)

    def test_order_null_fields(self):
        self.client.get_resource = MagicMock(return_value=self.mock_minimal_order_json)
        o = Order.get(1)
        self.assertEqual(o.billing_info, None)
        self.assertEqual(o.shipping_info, None)
        self.assertEqual(o.payment_details.payment_type, None)
        self.assertEqual(o.shipping_option, None)

    def test_date_fmt(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        oi = o.order_items[0]
        self.assertEqual(2020, oi.ships_on_dt.year)
        self.assertEqual(12, oi.ships_on_dt.month)
        self.assertEqual(28, oi.ships_on_dt.day)
        self.assertEqual(2020, o.created_dt.year)
        self.assertEqual(12, o.created_dt.month)
        self.assertEqual(8, o.created_dt.day)

    def test_ship_desc(self):
        from paperless.objects.orders import ShippingOption
        import datetime

        dt = datetime.datetime.now()

        # pickup
        so1 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            shipping_method=None,
            type='pickup',
        )
        self.assertTrue(
            so1.summary(dt, '').startswith(
                'Customer will pickup from supplier\'s location.'
            )
        )

        # customer's account
        so2 = ShippingOption(
            customers_account_number='12345',
            customers_carrier='ups',
            shipping_method='ground',
            type='customers_shipping_account',
        )
        self.assertIn('Use Customer\'s Shipping Account', so2.summary(dt, ''))
        self.assertIn('Method: GROUND', so2.summary(dt, ''))

        # supplier's account
        so3 = ShippingOption(
            customers_account_number=None,
            customers_carrier=None,
            shipping_method='ground',
            type='suppliers_shipping_account',
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
            114384,
            114390,
            114389,
            114391,
            114388,
            114387,
            114386,
            114385,
        ]
        self.assertEqual(expected_order, [c.component.id for c in assm])
        self.assertEqual(2, assm[4].level)
        self.assertEqual(4, assm[4].level_count)

    def test_billing_info(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        billing_info = o.billing_info
        self.assertEqual(billing_info.address1, "1 FISKE TER")
        self.assertEqual(billing_info.address2, "")
        self.assertEqual(billing_info.business_name, "Outside Firm")
        self.assertEqual(billing_info.city, "BOSTON")
        self.assertEqual(billing_info.country, "USA")
        self.assertEqual(billing_info.attention, "Test Customer")
        self.assertEqual(billing_info.phone, "5555555555")
        self.assertEqual(billing_info.phone_ext, "")
        self.assertEqual(billing_info.postal_code, "02134-4503")
        self.assertEqual(billing_info.state, "MA")

    def test_contact(self):
        self.client.get_resource = MagicMock(return_value=self.mock_minimal_order_json)
        o = Order.get(1)
        c = o.contact
        a = c.account
        self.assertEqual(c.id, 3545)
        self.assertEqual(c.first_name, "Test")
        self.assertEqual(c.last_name, "Customer")
        self.assertEqual(c.email, "rob.carrington+outsidefirm@paperlessparts.com")
        self.assertIsNone(c.notes)
        self.assertEqual(a.id, 1986)
        self.assertIsNone(a.notes)
        self.assertEqual(a.name, "Outside Firm"),
        self.assertEqual(a.erp_code, "OUTFIRM")
        self.assertEqual(a.payment_terms, "Net 30")
        self.assertEqual(a.payment_terms_period, 30)
        self.assertEqual(c.phone, "")
        self.assertEqual(c.phone_ext, "")

    def test_customer(self):
        self.client.get_resource = MagicMock(return_value=self.mock_minimal_order_json)
        o = Order.get(1)
        cu = o.customer
        co = cu.company
        self.assertIsNone(cu.id)
        self.assertEqual(cu.first_name, "Test")
        self.assertEqual(cu.last_name, "Customer")
        self.assertEqual(cu.email, "rob.carrington+outsidefirm@paperlessparts.com")
        self.assertIsNone(cu.notes)
        self.assertIsNone(co.id)
        self.assertEqual(co.business_name, "Outside Firm")
        self.assertEqual(co.erp_code, "OUTFIRM")
        self.assertEqual(cu.phone, "")
        self.assertEqual(cu.phone_ext, "")

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

    def test_shipping_info(self):
        self.client.get_resource = MagicMock(return_value=self.mock_order_json)
        o = Order.get(1)
        shipping_info = o.shipping_info
        self.assertEqual(shipping_info.address1, "1 FISKE TER")
        self.assertEqual(shipping_info.address2, "")
        self.assertEqual(shipping_info.business_name, "Outside Firm")
        self.assertEqual(shipping_info.city, "BOSTON")
        self.assertEqual(shipping_info.country, "USA")
        self.assertEqual(shipping_info.attention, "Cus Tomer")
        self.assertEqual(shipping_info.phone, "5555555555")
        self.assertEqual(shipping_info.phone_ext, "")
        self.assertEqual(shipping_info.postal_code, "02134-4503")
        self.assertEqual(shipping_info.state, "MA")
