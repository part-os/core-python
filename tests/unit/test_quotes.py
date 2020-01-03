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
        self.assertEqual(q.number, 67)
        self.assertEqual(q.tax_rate, 0.)
        self.assertFalse(q.is_unviewed_drafted_rfq)
        # test customer
        customer = q.customer
        self.assertEqual(customer.last_name, 'Customer')
        # test company
        company = customer.company
        self.assertEqual(company.business_name, 'Outside Firm')
        # test metrics
        metrics = company.metrics
        self.assertEqual(metrics.order_revenue_all_time.dollars, Decimal('4359.38'))
        # test quote items
        quote_item = q.quote_items[0]
        self.assertEqual(quote_item.id, 24988)
        self.assertEqual(quote_item.type, 'automatic')
        self.assertEqual(quote_item.component_ids[0], 28600)
        # test root component
        root_component = quote_item.root_component
        self.assertEqual(root_component.id, 28600)
        self.assertEqual(root_component.type, 'assembled')
        self.assertEqual(root_component.part.filename, 'small-sub-assembly.STEP')
        # test quantities
        quantity = root_component.quantities[0]
        self.assertEqual(quantity.quantity, 1)
        self.assertEqual(quantity.unit_price.dollars, Decimal('3086.88'))
        # test operations
        operation = root_component.operations[0]
        self.assertEqual(operation.name, 'Chromate')
        # test process
        process = root_component.process
        self.assertEqual(process.name, 'CNC Machining')
        # test material
        material = root_component.material
        self.assertEqual(material.name, 'Aluminium 6061')
        # test expedites
        expedite = q.quote_items[2].root_component.quantities[0].expedites[0]
        self.assertEqual(expedite.unit_price.dollars, 65.)



