
from paperless.main import PaperlessSDK
from paperless.listeners import OrderListener

from paperless.mixins import UpdateMixin

from paperless.objects.address import Address
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from paperless.objects.contacts import CompanyContact, CustomerContact, PaymentTerms

from paperless.client import PaperlessClient


import attr

my_client = PaperlessClient(
    access_token='5e6f3e8b0395ebea51a2d855894f308f19d8df18'
)

"""
TESTING PAYMENT TERMS
"""
"""
print(PaymentTerms.list())
"""
"""
TESTING CREATE CUSTOMER
"""
"""
test_shipping_address = Address(
    address1="133 Portland St",
    business_name="Test Shipping Dept",
    city="Boston",
    country="USA",
    first_name="Shippo",
    last_name="Hippo",
    phone=1234567890,
    postal_code="02134",
    state="MA"
)
test_billing_address = Address(
    address1="137 Portland St",
    business_name="Test Accts Payable Dept",
    city="Boston",
    country="USA",
    first_name="Accountant",
    last_name="Dude",
    phone=1234567890,
    postal_code="02134",
    state="MA"
)
minimum_customer_contact = CustomerContact(
    email="william+minimalemail4@paperlessparts.com",
    first_name="William",
    last_name="Headrick"
)
print(minimum_customer_contact.to_json())
#test_customer_contact.save()

payment_term = PaymentTerms.list()[0]

complete_customer_contact = CustomerContact(
    billing_info=test_billing_address,
    email="william+minimalemail8@paperlessparts.com",
    first_name="William",
    last_name="Headrick",
    payment_terms=payment_term,
    shipping_info=test_shipping_address
)
print(complete_customer_contact.to_json())
complete_customer_contact.create(


print("test_customer_contact")
#print(test_customer_contact)
"""

"""
TEST CREATE COMPANY
"""
"""
payment_term = PaymentTerms.list()[0]

minimum_company = CompanyContact(
    business_name="minimum business name 19",
)
created_company = minimum_company.create()
print("create result")
print(minimum_company)

minimum_company.payment_terms = payment_term
print("before update")
print(minimum_company)
minimum_company.update()
print("after update")
print(minimum_company)

minimum_customer_contact = CustomerContact(
    email="william+minimalemail51@paperlessparts.com",
    first_name="William",
    last_name="Headrick",
    company=minimum_company
)
minimum_customer_contact.create()
"""
"""
TESTING GET OBJECT
"""
"""
test = Order.get(52)
order_list = Order.list()
print("order list")
print(order_list)
"""


"""
TESTING LISTENERS!
"""
#test = Address(**{'address1': '15 MAIN ST', 'address2': '', 'business_name': 'MAS Product Development Inc.', 'city': 'NASHU', 'country': 'USA', 'first_name': 'Matt', 'last_name': 'Sordillo', 'phone': '', 'phone_ext': '', 'postal_code': '03064-2728', 'state': 'NH'})
#print(test)

"""
from tests.factories.orders import OperationFactory, OrderFactory, OrderItemFactory

dummy_order1 = OrderFactory.build()
print(dummy_order1.number)

number = 404
dummy_order2 = OrderFactory.build(number=number)
print(dummy_order2.number)
assert dummy_order2.number == number

dummy_operations = OperationFactory.build_batch(10)
print(dummy_operations)
dummy_order_item = OrderItemFactory.build(operations=dummy_operations)
print(dummy_order_item)
"""
# test = Order.get(2)
# print(test.to_dict())
# test = Quote.get(4)
test = Quote.get_new(2)
print(test)
"""
class MyOrderListener(OrderListener):
    def on_event(self, resource):
        print("on event")
        print(resource)
        print(resource.to_dict())


order_list = Order.list(params={'o': '-number'})
print(order_list)
my_sdk = PaperlessSDK()
#my_sdk.add_listener(MyOrderListener(last_updated=30))
my_sdk.add_listener(MyOrderListener())
my_sdk.run()

#test = Order.get(52)
#print(getattr(test, 'number', 'WIALLIAM!!!!!'))
print("test")
#print(test)
print("to dict")
#print(test.to_dict())
"""
