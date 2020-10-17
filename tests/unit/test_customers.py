import unittest
import json
from paperless.client import PaperlessClient
from unittest.mock import MagicMock

#test customer with company create has a company_id in it
#test customer with payment terms has payment_terms_id in it
#test customer created has a new id
#test primary key is number
from paperless.objects.common import Money
from paperless.objects.customers import Customer, Company


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/customer.json') as data_file:
            self.mock_customer_json = json.load(data_file)

    def test_get_customer(self):
        self.client.get_resource = MagicMock(return_value=self.mock_customer_json)
        c = Customer.get(1)
        self.assertEqual(c.billing_info.address1, "1 City Hall Sq.")
        self.assertEqual(c.billing_info.address2, None)
        self.assertEqual(c.billing_info.business_name, "Paperless Parts, Inc.")
        self.assertEqual(c.billing_info.city, "Boston")
        self.assertEqual(c.billing_info.country, "USA")
        self.assertEqual(c.billing_info.first_name, "Gordon")
        self.assertEqual(c.billing_info.last_name, "Moore")
        self.assertEqual(c.billing_info.phone, "6175555555")
        self.assertEqual(c.billing_info.phone_ext, None)
        self.assertEqual(c.billing_info.postal_code, "02108")
        self.assertEqual(c.billing_info.state, "MA")
        self.assertEqual(c.business_name, "Paperless Parts, Inc.")
        self.assertEqual(c.company_erp_code, "PPI")
        self.assertEqual(c.company_id, 17)
        self.assertEqual(c.created, "2020-08-25T18:00:53+00:00")
        self.assertEqual(c.credit_line, Money(raw_amount=10000))
        self.assertEqual(c.email, "careers@paperlessparts.com")
        self.assertEqual(c.first_name, "Gordon")
        self.assertEqual(c.id, 137)
        self.assertEqual(c.last_name, "Moore")
        self.assertEqual(c.notes, None)
        self.assertEqual(c.payment_terms, "Net 30")
        self.assertEqual(c.payment_terms_period, 30)
        self.assertEqual(c.phone, "6175555555")
        self.assertEqual(c.phone_ext, None)
        self.assertTrue(c.purchase_orders_enabled)
        self.assertEqual(c.shipping_info.address1, "1 City Hall Sq.")
        self.assertEqual(c.shipping_info.address2, None)
        self.assertEqual(c.shipping_info.business_name, "Paperless Parts, Inc.")
        self.assertEqual(c.shipping_info.city, "Boston")
        self.assertEqual(c.shipping_info.country, "USA")
        self.assertEqual(c.shipping_info.first_name, "Gordon")
        self.assertEqual(c.shipping_info.last_name, "Moore")
        self.assertEqual(c.shipping_info.phone, "6175555555")
        self.assertEqual(c.shipping_info.phone_ext, None)
        self.assertEqual(c.shipping_info.postal_code, "02108")
        self.assertEqual(c.shipping_info.state, "MA")
        self.assertTrue(c.tax_exempt)
        self.assertEqual(c.tax_rate, 6.25)
        self.assertEqual(c.url, "https://www.paperlessparts.com")

    def test_convert_customer_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_customer_json)
        self.maxDiff = 2000
        c = Customer.get(1)
        expected_customer_json = {
            "company_id": 17,
            "credit_line": 10000.0,
            "email": "careers@paperlessparts.com",
            "first_name": "Gordon",
            "last_name": "Moore",
            "notes": None,
            "payment_terms": "Net 30",
            "payment_terms_period": 30,
            "phone": "6175555555",
            "phone_ext": None,
            "purchase_orders_enabled": True,
            "salesperson": None,
            "tax_exempt": True,
            "tax_rate": 6.25,
            "url": "https://www.paperlessparts.com",
        }
        self.assertEqual(c.to_json(), json.dumps(expected_customer_json))


class TestCompany(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/company.json') as data_file:
            self.mock_company_json = json.load(data_file)

    def test_get_company(self):
        self.client.get_resource = MagicMock(return_value=self.mock_company_json)
        c = Company.get(1)
        self.assertEqual(c.billing_info.address1, "1 City Hall Sq.")
        self.assertEqual(c.billing_info.address2, None)
        self.assertEqual(c.billing_info.business_name, "Accolades R Us")
        self.assertEqual(c.billing_info.city, "Boston")
        self.assertEqual(c.billing_info.country, "USA")
        self.assertEqual(c.billing_info.first_name, "Gordon")
        self.assertEqual(c.billing_info.last_name, "Moore")
        self.assertEqual(c.billing_info.phone, "6175555555")
        self.assertEqual(c.billing_info.phone_ext, None)
        self.assertEqual(c.billing_info.postal_code, "02108")
        self.assertEqual(c.billing_info.state, "MA")
        self.assertEqual(c.business_name, "Accolades R Us Engineering")
        self.assertEqual(c.erp_code, "PPI")
        self.assertEqual(c.created, "2020-05-08T15:14:14+00:00")
        self.assertEqual(c.credit_line, Money(raw_amount=3000))
        self.assertEqual(c.id, 4551)
        self.assertEqual(c.notes, None)
        self.assertEqual(c.payment_terms, "Net 30")
        self.assertEqual(c.payment_terms_period, 30)
        self.assertEqual(c.phone, None)
        self.assertEqual(c.phone_ext, None)
        self.assertTrue(c.purchase_orders_enabled)
        self.assertEqual(c.shipping_info.address1, "1 City Hall Sq.")
        self.assertEqual(c.shipping_info.address2, None)
        self.assertEqual(c.shipping_info.business_name, "Accolades R Us")
        self.assertEqual(c.shipping_info.city, "Boston")
        self.assertEqual(c.shipping_info.country, "USA")
        self.assertEqual(c.shipping_info.first_name, "Gordon")
        self.assertEqual(c.shipping_info.last_name, "Moore")
        self.assertEqual(c.shipping_info.phone, "6175555555")
        self.assertEqual(c.shipping_info.phone_ext, None)
        self.assertEqual(c.shipping_info.postal_code, "02108")
        self.assertEqual(c.shipping_info.state, "MA")
        self.assertEqual(c.slug, "accolades-r-us-engineering")
        self.assertTrue(c.tax_exempt)
        self.assertEqual(c.tax_rate, None)
        self.assertEqual(c.url, "https://www.paperlessparts.com")


    def test_convert_company_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_company_json)
        self.maxDiff = 2000
        c = Company.get(1)
        expected_company_json = {
            "business_name": "Accolades R Us Engineering",
            "credit_line": 3000.0,
            "erp_code": "PPI",
            "notes": None,
            "payment_terms": "Net 30",
            "payment_terms_period": 30,
            "phone": None,
            "phone_ext": None,
            "tax_rate": None,
            "slug": "accolades-r-us-engineering",
            "url": "https://www.paperlessparts.com",
            "purchase_orders_enabled": True,
            "tax_exempt": True,
        }
        self.assertEqual(c.to_json(), json.dumps(expected_company_json))

