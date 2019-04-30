
from paperless.main import PaperlessSDK
from paperless.listeners import OrderListener

from paperless.mixins import UpdateMixin

from paperless.objects.address import Address
from paperless.objects.orders import Order
from paperless.objects.contacts import CustomerContact, PaymentTerms

from paperless.client import PaperlessClient


import attr

print("HELLO WILLIAM")

"""
TESTING PAYMENT TERMS
"""
"""
my_client = PaperlessClient(
    username='jason@paperlessparts.com',
    password='P@perless2',
    group_slug='a-cut-above-cnc',
    version=PaperlessClient.VERSION_0,
    base_url="https://dev.paperlessparts.com/api"
)
print(PaymentTerms.list())
"""
"""
TESTING CREATE CUSTOMER
"""
my_client = PaperlessClient(
    username='jason@paperlessparts.com',
    password='P@perless2',
    group_slug='a-cut-above-cnc',
    version=PaperlessClient.VERSION_0,
    base_url="https://dev.paperlessparts.com/api"
)

test_shipping_address = Address(
    business_name="Test Shipping Dept",
    city="Boston",
    country="USA",
    first_name="Shippo",
    last_name="Hippo",
    line1="133 Portland St",
    phone=1234567890,
    postal_code="02134",
    state="MA"
)
test_billing_address = Address(
    business_name="Test Accts Payable Dept",
    city="Boston",
    country="USA",
    first_name="Accountant",
    last_name="Dude",
    line1="137 Portland St",
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
complete_customer_contact = CustomerContact(
    billing_info=test_billing_address,
    email="william+minimalemail4@paperlessparts.com",
    first_name="William",
    last_name="Headrick",
    shipping_info=test_shipping_address
)
print(complete_customer_contact.to_json())
complete_customer_contact.save()
"""for attr, value in test_customer_contact.__dict__.items():
    print("attr")
    print(attr)
    print("value")
    print(value)
    print("isinstance(value, UpdateMixin)")
    print(isinstance(value, UpdateMixin))"""


print("test_customer_contact")
#print(test_customer_contact)


"""
TESTING GET OBJECT
"""
"""
my_client = PaperlessClient(
    username='jason@paperlessparts.com',
    password='P@perless2',
    group_slug='a-cut-above-cnc',
    version=PaperlessClient.VERSION_0,
    base_url="https://dev.paperlessparts.com/api"
)
test = Order.get(52)
order_list = Order.list()
print("order list")
print(order_list)
"""


"""
TESTING LISTENERS!
"""
"""
class MyOrderListener(OrderListener):
    def on_event(self, resource):
        print("on event")
        print(resource)
        print(resource.to_dict())

my_client = PaperlessClient(
    username='jason@paperlessparts.com',
    password='P@perless2',
    group_slug='a-cut-above-cnc',
    version=PaperlessClient.VERSION_0,
    base_url="https://dev.paperlessparts.com/api"
)

my_sdk = PaperlessSDK()
my_sdk.add_listener(MyOrderListener(last_updated=30))
my_sdk.run()

#test = Order.get(52)
#print(getattr(test, 'number', 'WIALLIAM!!!!!'))
print("test")
#print(test)
print("to dict")
#print(test.to_dict())
"""

