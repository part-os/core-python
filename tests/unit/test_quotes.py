import json
import unittest
from decimal import Decimal
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.quotes import Quote


class TestQuotes(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/quote.json') as data_file:
            self.mock_quote_json = json.load(data_file)

    def test_get_quote(self):
        self.client.get_resource = MagicMock(return_value=self.mock_quote_json)
        q = Quote.get(1)
        self.assertEqual(q.number, 339)
        self.assertEqual(q.tax_rate, 0.0)
        self.assertFalse(q.is_unviewed_drafted_rfq)
        # test customer
        customer = q.customer
        self.assertIsNone(customer.id)
        self.assertEqual(customer.first_name, 'Test')
        self.assertEqual(customer.last_name, 'Customer')
        self.assertEqual(
            customer.email, 'rob.carrington+outsidefirm@paperlessparts.com'
        )
        self.assertIsNone(customer.notes)
        # test company
        company = customer.company
        self.assertIsNone(company.id)
        self.assertEqual(company.business_name, 'Outside Firm')
        self.assertEqual(company.erp_code, 'OUTFIRM')
        self.assertIsNone(company.notes)
        contact = q.contact
        # test contact
        self.assertEqual(contact.id, 3545)
        self.assertEqual(contact.first_name, 'Test')
        self.assertEqual(contact.last_name, 'Customer')
        self.assertEqual(contact.email, 'rob.carrington+outsidefirm@paperlessparts.com')
        self.assertIsNone(contact.notes)
        # test account
        account = contact.account
        self.assertEqual(account.id, 1986)
        self.assertIsNone(account.notes)
        self.assertEqual(account.name, 'Outside Firm')
        self.assertEqual(account.erp_code, 'OUTFIRM')
        # test salesperson
        sales_person = q.sales_person
        self.assertEqual(sales_person.first_name, 'Heathrow Chester')
        # test estimator
        estimator = q.estimator
        self.assertEqual(estimator.first_name, 'Heathrow Chester')
        # test metrics
        metrics = company.metrics
        self.assertEqual(metrics.order_revenue_all_time.dollars, Decimal('42691.43'))
        # test quote items
        quote_item = q.quote_items[0]
        self.assertEqual(quote_item.type, 'automatic')
        self.assertEqual(len(quote_item.component_ids), 8)
        # test root component
        root_component = quote_item.root_component
        self.assertEqual(root_component.type, 'assembled')
        self.assertEqual(root_component.part_name, 'small-sub-assembly.STEP')
        self.assertFalse(
            root_component.part_custom_attrs
        )  # Note - this could either be None or a list, this confirms it is either None or an empty list
        # test addons
        add_on = root_component.add_ons[0]
        self.assertEqual(add_on.is_required, True)
        add_on_quantity = add_on.quantities[0]
        self.assertEqual(add_on_quantity.manual_price.dollars, Decimal('1000'))
        # test quantities
        quantity = root_component.quantities[0]
        self.assertEqual(quantity.quantity, 1)
        self.assertEqual(quantity.unit_price.dollars, Decimal('2616.74'))
        self.assertEqual(
            quantity.total_price_with_required_add_ons.dollars, Decimal('3616.74')
        )
        # test operations
        operation = root_component.shop_operations[0]
        self.assertEqual(operation.name, 'Chromate')
        self.assertEqual(operation.operation_definition_name, 'Chromate')
        operation_quantity = operation.quantities[0]
        self.assertEqual(operation_quantity.price.dollars, 150)

        # test all costing variables
        costing_variable = operation.costing_variables[3]
        self.assertEqual(
            costing_variable.quantities[operation.quantities[0].quantity].value,
            '304-#4',
        )
        self.assertEqual(
            costing_variable.quantities[operation.quantities[0].quantity].row,
            {
                'diameter': 4.0,
                'length': 48.0,
                'material': '304-#4',
                'requires_prep': True,
                'row_number': 3,
            },
        )
        self.assertEqual(
            costing_variable.quantities[operation.quantities[1].quantity].value,
            '304-#4',
        )
        self.assertEqual(
            costing_variable.quantities[operation.quantities[1].quantity].row,
            {
                'diameter': 4.0,
                'length': 48.0,
                'material': '304-#4',
                'requires_prep': True,
                'row_number': 3,
            },
        )
        self.assertIsNone(
            costing_variable.quantities[operation.quantities[1].quantity].options
        )
        vp = operation.get_variable_for_qty(
            'Lot Charge', operation.quantities[0].quantity
        )
        self.assertEqual(vp.value, 150)
        self.assertIsNone(vp.row)
        self.assertIsNone(vp.options)

        comp = q.quote_items[1].root_component
        qty_specific_op = comp.shop_operations[7]
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[0].quantity
            ).value,
            2,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[1].quantity
            ).value,
            5,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[2].quantity
            ).value,
            10,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Num', qty_specific_op.quantities[3].quantity
            ).value,
            25,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[0].quantity
            ).value,
            'a',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[1].quantity
            ).value,
            'b',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[2].quantity
            ).value,
            'c',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Basic Str', qty_specific_op.quantities[3].quantity
            ).value,
            'd',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[0].quantity
            ).value,
            '2',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[0].quantity
            ).options,
            ['1', '2', '3'],
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[1].quantity
            ).value,
            '5',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[1].quantity
            ).options,
            ['1', '2', '3', '5'],
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[2].quantity
            ).value,
            '10',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[2].quantity
            ).options,
            ['1', '2', '3', '10'],
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[3].quantity
            ).value,
            '25',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Drop Down Num', qty_specific_op.quantities[3].quantity
            ).options,
            ['1', '2', '3', '25'],
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[0].quantity
            ).value,
            '6061-T6',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[0].quantity
            ).row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[1].quantity
            ).value,
            'Ti6Al4V',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[1].quantity
            ).row,
            {
                'diameter': 5.0,
                'length': 24.0,
                'material': 'Ti6Al4V',
                'requires_prep': True,
                'row_number': 4,
            },
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[2].quantity
            ).value,
            'A2',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[2].quantity
            ).row,
            {
                'diameter': 6.0,
                'length': 48.0,
                'material': 'A2',
                'requires_prep': False,
                'row_number': 5,
            },
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[3].quantity
            ).value,
            '6061-T6',
        )
        self.assertEqual(
            qty_specific_op.get_variable_for_qty(
                'Material Selection', qty_specific_op.quantities[3].quantity
            ).row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )

        # test addon costing variables
        qty_specific_ao = comp.add_ons[0]
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[0].quantity
            ).value,
            2,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[1].quantity
            ).value,
            5,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[2].quantity
            ).value,
            10,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Num', qty_specific_ao.quantities[3].quantity
            ).value,
            25,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[0].quantity
            ).value,
            'a',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[1].quantity
            ).value,
            'b',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[2].quantity
            ).value,
            'c',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Basic Str', qty_specific_ao.quantities[3].quantity
            ).value,
            'd',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[0].quantity
            ).value,
            '2',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[0].quantity
            ).row,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[0].quantity
            ).options,
            ['1', '2', '3'],
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[1].quantity
            ).value,
            '5',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[1].quantity
            ).options,
            ['1', '2', '3', '5'],
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[2].quantity
            ).value,
            '10',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[2].quantity
            ).options,
            ['1', '2', '3', '10'],
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[3].quantity
            ).value,
            '25',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Drop Down Num', qty_specific_ao.quantities[3].quantity
            ).options,
            ['1', '2', '3', '25'],
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[0].quantity
            ).value,
            '6061-T6',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[0].quantity
            ).row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[0].quantity
            ).options,
            None,
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[1].quantity
            ).value,
            'Ti6Al4V',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[1].quantity
            ).row,
            {
                'diameter': 5.0,
                'length': 24.0,
                'material': 'Ti6Al4V',
                'requires_prep': True,
                'row_number': 4,
            },
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[2].quantity
            ).value,
            'A2',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[2].quantity
            ).row,
            {
                'diameter': 6.0,
                'length': 48.0,
                'material': 'A2',
                'requires_prep': False,
                'row_number': 5,
            },
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[3].quantity
            ).value,
            '6061-T6',
        )
        self.assertEqual(
            qty_specific_ao.get_variable_for_qty(
                'Material Selection', qty_specific_ao.quantities[3].quantity
            ).row,
            {
                'diameter': 1.0,
                'length': 24.0,
                'material': '6061-T6',
                'requires_prep': False,
                'row_number': 0,
            },
        )

        # test process
        process = root_component.process
        self.assertEqual(process.name, 'CNC Machining')
        # test material
        material = root_component.material
        self.assertEqual(material.name, 'Aluminium 6061')
        # test expedites
        expedite = q.quote_items[2].root_component.quantities[0].expedites[0]
        self.assertEqual(expedite.unit_price.dollars, 65.0)
        # test parent quote
        parent_quote = q.parent_quote
        self.assertEqual(parent_quote.number, 194)
        # test parent supplier order
        parent_supplier_order = q.parent_supplier_order
        self.assertIsNone(parent_supplier_order)
        # test purchased component
        purchased_components = [c for c in quote_item.components if c.is_hardware]
        self.assertEqual(1, len(purchased_components))
        pc = purchased_components[0]
        self.assertEqual('AC-M6-2', pc.purchased_component.oem_part_number)
        self.assertIsNone(pc.purchased_component.internal_part_number)
        self.assertIsNone(pc.purchased_component.description)
        self.assertEqual(
            Decimal('0.9310'), pc.purchased_component.piece_price.raw_amount
        )
        self.assertEqual(Decimal('0.93'), pc.purchased_component.piece_price.dollars)
        self.assertEqual(pc.purchased_component.get_property('brand'), "Penn")
        self.assertEqual(pc.purchased_component.get_property('lead_time'), 4)
        self.assertEqual(pc.purchased_component.get_property('in_stock'), True)
        self.assertIsNone(pc.purchased_component.get_property("bad_name"))
