Paperless Entities
==================

The Paperless SDK comes with predefined Classes that allow you to perform basic CRUDL (Create, Read, Update, Delete, and List) operations.

Examples
--------
.. code-block:: python

    from paperless.client import PaperlessClient

    from paperless.objects.customers import Customer, Company
    from paperless.objects.address import Address
    from paperless.objects.orders import Order

    # you must initiate the client before performing these interations
    PaperlessClient(...)

    # List your Customers
    customer_list = Customer.list()

    # Filter Customer list
    Customer.filter(company_erp_code='PPI', company_id=45)

    #Search Customers
    Customer.search(search_term='bill@paperlessparts.com')

    # Create a customer with fewest required fields
    minimum_customer = Customer(
        company_id=45
        first_name="John",
        last_name="Smith",
        email="john@paperlessparts.com"
    )
    minimum_customer.create()

    #Create a customer with all fields
    complete_customer = Customer(
        company_id=45,
        first_name="John",
        last_name="Smith",
        email="john@paperlessparts.com",
        credit_line=10000.00,
        notes="Customer notes",
        payment_terms="Net 30",
        payment_terms_period=30,
        phone="5555555555"
        phone_ext="123"
        purchase_orders_enabled=True,
        tax_exempt=False,
        tax_rate=6.5,
        url="www.paperlessparts.com"
    )
    complete_customer.create()

    #update a customer
    complete_customer.first_name = "Jonathan"
    complete_customer.update()

    #add shipping info to customer
    shipping_info = AddressInfo(
        address1="133 Portland St",
        adresss2=None
        business_name="Shipping Dept",
        city="Boston",
        country="USA",
        first_name="Paperless",
        last_name="Paddy",
        phone=1234567890,
        phone_ext="123",
        postal_code="02134",
        state="MA"
    )
    complete_customer.set_shipping_info(shipping_info) #returns AddressInfo object

    # add billing info to customer
    billing_info = Address(
        address1="137 Portland St",
        address2=None,
        business_name="Test Accts Payable Dept",
        city="Boston",
        country="USA",
        first_name="Accountant",
        last_name="Dude",
        phone="1234567890",
        phone_ext="123",
        postal_code="02134",
        state="MA"
    )
    complete_customer.set_billing_info(billing_info) #returns AddressInfo object

    # Create company with fewest fields
    minimum_company = Company(
        business_name="Paperless Parts Inc.",
    )
    minimum_company.create()

    #Create a company with all fields
    complete_company = Company(
        business_name="Paperless Parts Inc.",
        credit_line=10000.00,
        erp_code="PPI",
        notes="Company Notes",
        phone="5555555555",
        phone_ext="123",
        payment_terms="Net 30",
        payment_terms_period=30,
        purchase_orders_enabled=True,
        slug="paperless-parts-inc",
        tax_exempt=False,
        tax_rate=6.25,
        url="www.paperlessparts.com",
    )
    complete_company.create()

    #update a company
    complete_company.notes = "Updated company notes"
    complete_company.update()


    #add shipping info to company
    shipping_info = AddressInfo(
        address1="133 Portland St",
        address2=None,
        business_name="Shipping Dept",
        city="Boston",
        country="USA",
        first_name="Paperless",
        last_name="Paddy",
        phone="1234567890",
        phone_ext="123",
        postal_code="02134",
        state="MA"
    )
    complete_company.set_shipping_info(shipping_info) #returns AddressInfo object

    # add billing info to company
    billing_info = Address(
        address1="137 Portland St",
        address2=None
        business_name="Test Accts Payable Dept",
        city="Boston",
        country="USA",
        first_name="Accountant",
        last_name="Dude",
        phone="1234567890",
        phone_ext="123",
        postal_code="02134",
        state="MA"
    )
    complete_company.set_billing_info(billing_info) #returns


    # Get and order
    order = Order.get(52)

    # List orders
    order_list = Order.list()

Supported Contact Entities
--------------------------
.. autoclass:: paperless.objects.customers.AddressInfo
    :members:
    :undoc-members:
    :exclude-members: construct_list_url, parse_list_response, construct_post_url, from_json_to_dict
    :show-inheritance:
    :inherited-members:

.. autoclass:: paperless.objects.customers.Company
    :members:
    :undoc-members:
    :exclude-members: construct_patch_url, construct_post_url, from_json_to_dict
    :show-inheritance:
    :inherited-members:

.. autoclass:: paperless.objects.customers.Customer
    :members:
    :undoc-members:
    :exclude-members: construct_patch_url, construct_post_url, from_json_to_dict
    :show-inheritance:
    :inherited-members:

Supported Order Entities
------------------------
.. autoclass:: paperless.objects.orders.Order
    :members:
    :undoc-members:
    :exclude-members: construct_get_url, construct_list_url, construct_get_params, parse_list_response, from_json_to_dict
    :show-inheritance:
    :inherited-members: to_dict, list, from_json, get

**Non-CRUDL Order Entities**

.. autoclass:: paperless.objects.orders.Operation
    :members:
    :undoc-members:

.. autoclass:: paperless.objects.orders.OrderItem
    :members:
    :undoc-members:

.. autoclass:: paperless.objects.orders.PaymentDetails
    :members:
    :undoc-members:

.. autoclass:: paperless.objects.orders.ShippingOption
    :members:
    :undoc-members:

.. autoclass:: paperless.objects.orders.OrderCustomer
    :members:
    :undoc-members:

.. autoclass:: paperless.objects.orders.OrderMinimum
    :members:
    :undoc-members:

