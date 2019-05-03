Paperless Entities
==================

The Paperless SDK comes with predefined Classes that allow you to perform basic CRUDL (Create, Read, Update, Delete, and List) operations.

Examples
--------
.. code-block:: python

    from paperless.client import PaperlessClient

    from paperless.objects.contacts import CompanyContact, CustomerContact, PaymentTerms
    from paperless.objects.address import Address
    from paperless.objects.orders import Order

    # you must initiate the client before performing these interations
    PaperlessClient(...)

    # List your payment terms
    payment_terms PaymentTerms.list()

    # Create a customer with fewest required fields
    minimum_customer_contact = CustomerContact(
        email="prison@boston.gov",
        first_name="Whitey",
        last_name="Bulger"
    )
    minimum_customer.create()

    # Create company with fewest fields
    minimum_company = CompanyContact(
        business_name="Mass Prison Authority",
    )
    minimum_company.create()

    # Create complete company
    shipping_address = Address(
        address1="133 Portland St",
        business_name="Shipping Dept",
        city="Boston",
        country="USA",
        first_name="Paperless",
        last_name="Paddy",
        phone=1234567890,
        postal_code="02134",
        state="MA"
    )
    billing_address = Address(
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

    payment_term = PaymentTerms.list()[0]

    complete_customer_contact = CustomerContact(
        billing_info=billing_address,
        company=minimum_company,
        email="prisoner@boston.gov",
        first_name="Whitey",
        last_name="Bulger",
        payment_terms=payment_term,
        shipping_info=shipping_address
    ).create()

    # Get and order
    order = Order.get(52)

    # List orders
    order_list = Order.list()

Supported Contact Entities
--------------------------
.. autoclass:: paperless.objects.contacts.PaymentTerms
    :members:
    :undoc-members:
    :exclude-members: construct_list_url, parse_list_response, construct_post_url
    :show-inheritance:
    :inherited-members:

.. autoclass:: paperless.objects.contacts.CompanyContact
    :members:
    :undoc-members:
    :exclude-members: construct_patch_url, construct_post_url
    :show-inheritance:
    :inherited-members:

.. autoclass:: paperless.objects.contacts.CustomerContact
    :members:
    :undoc-members:
    :exclude-members: construct_patch_url, construct_post_url
    :show-inheritance:
    :inherited-members:

Supported Order Entities
------------------------
.. autoclass:: paperless.objects.orders.Order
    :members:
    :undoc-members:
    :exclude-members: construct_get_url, construct_list_url, construct_get_params, parse_list_response
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
