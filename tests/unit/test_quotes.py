import unittest
import json
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
