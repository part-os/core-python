import unittest
import json
from paperless.client import PaperlessClient
from unittest.mock import MagicMock

#test customer with company create has a company_id in it
#test customer with payment terms has payment_terms_id in it
#test customer created has a new id
#test primary key is number
from paperless.objects.customers import Customer


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/customer.json') as data_file:
            self.mock_customer_json = json.load(data_file)

    def test_get_customer(self):
        self.client.get_resource = MagicMock(return_value=self.mock_customer_json)
        c = Customer.get(1)
        self.assertEqual(c.first_name, "Gordon")