import unittest
import json
from paperless.client import PaperlessClient
from unittest.mock import MagicMock

from paperless.objects.common import Money
from paperless.objects.customers import Contact, Account, BillingAddress, Facility


class TestContact(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/contact.json') as data_file:
            self.mock_contact_json = json.load(data_file)

    def test_get_contact(self):
        self.client.get_resource = MagicMock(return_value=self.mock_contact_json)
        c = Contact.get(1)
        self.assertEqual(c.account_id, 1)
        self.assertEqual(c.address.address1, "135 PORTLAND ST")
        self.assertIsNone(c.address.address2)
        self.assertEqual(c.address.city, "BOSTON")
        self.assertEqual(c.address.country, "USA")
        self.assertEqual(c.address.postal_code, "02114-1702")
        self.assertEqual(c.address.state, "MA")
        self.assertEqual(c.created, "2021-01-11T23:57:59.114838Z")
        self.assertEqual(c.email, "john.smith@paperlessparts.com")
        self.assertEqual(c.first_name, "John")
        self.assertEqual(c.id, 1)
        self.assertEqual(c.last_name, "Smith")
        self.assertEqual(c.notes, "test notes")
        self.assertEqual(c.phone, "6035555555")
        self.assertEqual(c.phone_ext, "")

    def test_convert_contact_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_contact_json)
        self.maxDiff = None
        c = Contact.get(1)
        expected_contact_json = {
            "account_id": 1,
            "email": "john.smith@paperlessparts.com",
            "first_name": "John",
            "last_name": "Smith",
            "notes": "test notes",
            "phone": "6035555555",
            "phone_ext": "",
            "address": {
                "address1": "135 PORTLAND ST",
                "address2": None,
                "city": "BOSTON",
                "country": "USA",
                "postal_code": "02114-1702",
                "state": "MA"
            },
            "salesperson": {
                "email": "william+stack_pusher@paperlessparts.com"
            }
        }
        self.assertEqual(c.to_json(), json.dumps(expected_contact_json))


class TestContactList(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/contact_list.json') as data_file:
            self.mock_contact_list_json = json.load(data_file)

    def test_get_customer_list(self):
        self.client.get_resource_list = MagicMock(return_value=self.mock_contact_list_json)
        c = Contact.list()
        self.assertEqual(len(c), 5)
        self.assertEqual(c[2].account_id, 1)
        self.assertEqual(c[2].created, "2021-01-11T23:58:15+00:00")
        self.assertEqual(c[2].email, "support+3@paperlessparts.com")
        self.assertEqual(c[2].first_name, "Ryan")
        self.assertEqual(c[2].id, 3)
        self.assertEqual(c[2].last_name, "Ryanson")
        self.assertEqual(c[2].phone, "9785555555")
        self.assertEqual(c[2].phone_ext, "")


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/account.json') as data_file:
            self.mock_account_json = json.load(data_file)

    def test_get_account(self):
        self.client.get_resource = MagicMock(return_value=self.mock_account_json)
        a = Account.get(1)
        ba = a.billing_addresses[0]
        sta = a.sold_to_address
        self.assertEqual(ba.address1, "1 City Hall Sq.")
        self.assertIsNone(ba.address2)
        self.assertEqual(ba.id, 138)
        self.assertEqual(ba.city, "Boston")
        self.assertEqual(ba.country, "USA")
        self.assertEqual(ba.postal_code, "02108")
        self.assertEqual(ba.state, "MA")
        self.assertEqual(a.created, "2021-01-11T23:57:59+00:00")
        self.assertEqual(a.credit_line, Money(raw_amount=30000))
        self.assertEqual(a.erp_code, "ARUE")
        self.assertEqual(a.id, 1)
        self.assertEqual(a.name, "Accolades R Us Engineering")
        self.assertIsNone(a.notes)
        self.assertEqual(a.payment_terms, "Net 30")
        self.assertEqual(a.payment_terms_period, 30)
        self.assertEqual(a.phone, "6035555555")
        self.assertIsNone(a.phone_ext)
        self.assertTrue(a.purchase_orders_enabled)
        self.assertEqual(sta.address1, "1 City Hall Sq.")
        self.assertIsNone(sta.address2)
        self.assertEqual(sta.city, "Boston")
        self.assertEqual(sta.country, "USA")
        self.assertEqual(sta.postal_code, "02108")
        self.assertEqual(sta.state, "MA")
        self.assertTrue(a.tax_exempt)
        self.assertIsNone(a.tax_rate)
        self.assertEqual(a.url, "https://www.paperlessparts.com")


    def test_convert_account_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_account_json)
        a = Account.get(1)
        expected_account_json = {
            "credit_line": 30000.0,
            "erp_code": "ARUE",
            "notes": None,
            "name": "Accolades R Us Engineering",
            "payment_terms": "Net 30",
            "payment_terms_period": 30,
            "phone": "6035555555",
            "phone_ext": None,
            "tax_exempt": True,
            "tax_rate": None,
            "url": "https://www.paperlessparts.com",
            "purchase_orders_enabled": True,
            "salesperson": {
                "email": "william+stack_pusher@paperlessparts.com"
            },
            "sold_to_address": {
                "address1": "1 City Hall Sq.",
                "address2": None,
                "city": "Boston",
                "country": "USA",
                "postal_code": "02108",
                "state": "MA",
            }
        }
        self.assertEqual(a.to_json(), json.dumps(expected_account_json))


class TestAccountList(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/account_list.json') as data_file:
            self.mock_account_list_json = json.load(data_file)

    def test_get_account_list(self):
        self.client.get_resource_list = MagicMock(return_value=self.mock_account_list_json)
        a = Account.list()
        self.assertEqual(len(a), 3)
        self.assertEqual(a[1].id, 2)
        self.assertEqual(a[1].name, "ACME Machining")
        self.assertEqual(a[1].phone, "6175555555")
        self.assertEqual(a[1].phone_ext, "12")


class TestBillingAddress(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/billing_address.json') as data_file:
            self.mock_billing_address_json = json.load(data_file)

    def test_get_billing_address(self):
        self.client.get_resource = MagicMock(return_value=self.mock_billing_address_json)
        ba = BillingAddress.get(1)
        self.assertEqual(ba.id, 1)
        self.assertEqual(ba.address1, "137 Portland St.")
        self.assertEqual(ba.address2, None)
        self.assertEqual(ba.city, "Boston")
        self.assertEqual(ba.country, "USA")
        self.assertEqual(ba.postal_code, "02114")
        self.assertEqual(ba.state, "MA")

    def test_convert_billing_address_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_billing_address_json)
        ba = BillingAddress.get(1)
        expected_billing_address_json = {
            "address1": "137 Portland St.",
            "address2": None,
            "city": "Boston",
            "country": "USA",
            "postal_code": "02114",
            "state": "MA",
        }
        self.assertEqual(ba.to_json(), json.dumps(expected_billing_address_json))


class TestFacility(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/facility.json') as data_file:
            self.mock_facility_json = json.load(data_file)

    def test_get_billing_address(self):
        self.client.get_resource = MagicMock(return_value=self.mock_facility_json)
        f = Facility.get(1)
        self.assertEqual(f.account_id, 1)
        self.assertEqual(f.address.address1, "137 Portland St.")
        self.assertEqual(f.address.address2, None)
        self.assertEqual(f.address.city, "Boston")
        self.assertEqual(f.address.country, "USA")
        self.assertEqual(f.address.postal_code, "02114")
        self.assertEqual(f.address.state, "MA")
        self.assertEqual(f.attention, "John Smith")
        self.assertEqual(f.id, 1)
        self.assertEqual(f.name, "Boston Office")

    def test_convert_facility_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_facility_json)
        f = Facility.get(1)
        expected_facility_json = {
            "account_id": 1,
            "attention": "John Smith",
            "name": "Boston Office",
            "address": {
                "address1": "137 Portland St.",
                "address2": None,
                "city": "Boston",
                "country": "USA",
                "postal_code": "02114",
                "state": "MA",
            },
            "salesperson": {
                "email": "william+stack_pusher@paperlessparts.com"
            }
        }
        self.assertEqual(f.to_json(), json.dumps(expected_facility_json))

