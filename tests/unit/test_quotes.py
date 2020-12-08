import unittest
import json
from decimal import Decimal
from unittest.mock import MagicMock

from paperless.objects.quotes import Quote
from paperless.client import PaperlessClient


class TestQuotes(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/quote.json') as data_file:
            self.mock_quote_json = json.load(data_file)

    def test_get_quote(self):
        self.client.get_resource = MagicMock(return_value=self.mock_quote_json)
        q = Quote.get(1)
        self.assertEqual(q.number, 194)
        self.assertEqual(q.tax_rate, 0.)
        self.assertFalse(q.is_unviewed_drafted_rfq)
        # test customer
        customer = q.customer
        self.assertEqual(customer.last_name, 'Customer')
        # test company
        company = customer.company
        self.assertEqual(company.business_name, 'Outside Firm')
        self.assertEqual(company.erp_code, 'OUTFIRM')
        # test salesperson
        sales_person = q.sales_person
        self.assertEqual(sales_person.first_name, 'Heathrow Chester')
        # test estimator
        estimator = q.estimator
        self.assertEqual(estimator.first_name, 'Heathrow Chester')
        # test metrics
        metrics = company.metrics
        self.assertEqual(metrics.order_revenue_all_time.dollars, Decimal('38246.19'))
        # test quote items
        quote_item = q.quote_items[0]
        self.assertEqual(quote_item.type, 'automatic')
        self.assertEqual(len(quote_item.component_ids), 8)
        # test root component
        root_component = quote_item.root_component
        self.assertEqual(root_component.type, 'assembled')
        self.assertEqual(root_component.part_name, 'small-sub-assembly.STEP')
        self.assertFalse(root_component.part_custom_attrs)  # Note - this could either be None or a list, this confirms it is either None or an empty list
        # TODO: quote add on costing variables, each type
        # test addons
        add_on = root_component.add_ons[0]
        self.assertEqual(add_on.is_required, True)
        add_on_quantity = add_on.quantities[0]
        self.assertEqual(add_on_quantity.manual_price.dollars, Decimal('1000'))
        # test quantities
        quantity = root_component.quantities[0]
        self.assertEqual(quantity.quantity, 1)
        self.assertEqual(quantity.unit_price.dollars, Decimal('2616.74'))
        self.assertEqual(quantity.total_price_with_required_add_ons.dollars, Decimal('3616.74'))
        # test operations
        operation = root_component.shop_operations[0]
        self.assertEqual(operation.name, 'Chromate')
        self.assertEqual(operation.operation_definition_name, 'Chromate')
        operation_quantity = operation.quantities[0]
        self.assertEqual(operation_quantity.price.dollars, 150)
        # TODO: quote operation costing variables, each type
        # test table costing variables
        costing_variable = operation.costing_variables[3]
        self.assertEqual(costing_variable.type, 'table')
        self.assertEqual(costing_variable.value, '304-#4')
        self.assertEqual(costing_variable.row, {'diameter': 4.0, 'length': 48.0, 'material': '304-#4', 'requires_prep': True, 'row_number': 3})
        self.assertEqual(costing_variable.quantities[operation.quantities[0].quantity].value, '304-#4')
        self.assertEqual(
            costing_variable.quantities[operation.quantities[0].quantity].row,
            {'diameter': 4.0, 'length': 48.0, 'material': '304-#4', 'requires_prep': True, 'row_number': 3},
        )
        self.assertEqual(costing_variable.quantities[operation.quantities[1].quantity].value, '304-#4')
        self.assertEqual(
            costing_variable.quantities[operation.quantities[1].quantity].row,
            {'diameter': 4.0, 'length': 48.0, 'material': '304-#4', 'requires_prep': True, 'row_number': 3},
        )
        self.assertIsNone(costing_variable.quantities[operation.quantities[1].quantity].options)
        vp = operation.get_variable_for_qty('Lot Charge', operation.quantities[0].quantity)
        self.assertEqual(vp.value, 150)
        self.assertIsNone(vp.row)
        self.assertIsNone(vp.options)
        # test process
        process = root_component.process
        self.assertEqual(process.name, 'CNC Machining')
        # test material
        material = root_component.material
        self.assertEqual(material.name, 'Aluminium 6061')
        # test expedites
        expedite = q.quote_items[2].root_component.quantities[0].expedites[0]
        self.assertEqual(expedite.unit_price.dollars, 65.)
        # test parent quote
        parent_quote = q.parent_quote
        self.assertEqual(parent_quote.number, 192)
        # test parent supplier order
        parent_supplier_order = q.parent_supplier_order
        self.assertIsNone(parent_supplier_order)
