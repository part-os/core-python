import datetime
import random
from decimal import Decimal

import factory.fuzzy
from faker import Faker

from paperless.objects.orders import (
    BaseOperation,
    Order,
    OrderCustomer,
    OrderItem,
    PaymentDetails,
    ShippingOption,
)

from .address import AddressFactory
from .fuzzies import (
    FuzzyDateString,
    FuzzyMaterialName,
    FuzzyOperationName,
    FuzzyPartFilename,
    FuzzyPhoneExt,
    FuzzyPhoneNumber,
)

# TODO: JUST USE FUZZY VALUES?
fake = Faker()


class OperationFactory(factory.Factory):
    class Meta:
        model = BaseOperation
        strategy = factory.BUILD_STRATEGY

    name = FuzzyOperationName()
    runtime = factory.fuzzy.FuzzyDecimal(0.1, 120.0)
    setup_time = factory.fuzzy.FuzzyDecimal(0.1, 120.0)


class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem
        strategy = factory.BUILD_STRATEGY

    description = fake.text(
        max_nb_chars=255
    )  # factory  limit, not guaranteed from Paperless Parts
    filename = FuzzyPartFilename()
    material = FuzzyMaterialName()
    operations = factory.List(
        [factory.SubFactory(OperationFactory) for _ in range(random.randrange(0, 8))]
    )
    part_number = fake.text(max_nb_chars=30)
    price = factory.fuzzy.FuzzyDecimal(1, 5000)
    private_notes = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
    public_notes = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
    quantity = factory.fuzzy.FuzzyInteger(1, 200)
    revision = fake.text(max_nb_chars=30)
    ships_on = FuzzyDateString(
        start_date=datetime.date.today() + datetime.timedelta(days=1),
        end_date=datetime.date.today() + datetime.timedelta(days=180),
    )
    unit_price = factory.LazyAttribute(lambda o: round(o.price / o.quantity, 2))


class PaymentDetailsFactory(factory.Factory):
    class Meta:
        model = PaymentDetails
        strategy = factory.BUILD_STRATEGY

    net_payout = factory.LazyAttribute(
        lambda p: None
        if p.payment_type == 'purchase_order'
        else round(p.price * Decimal(0.95), 2)
    )
    payment_type = factory.fuzzy.FuzzyChoice(choices=['credit_card', 'purchase_order'])
    purchase_order_number = factory.LazyAttribute(
        lambda p: None
        if p.payment_type == 'credit_card'
        else fake.text(max_nb_chars=15)
    )
    shipping_cost = factory.fuzzy.FuzzyDecimal(0, 200)
    subtotal = factory.fuzzy.FuzzyDecimal(200, 100000)
    tax_cost = factory.fuzzy.FuzzyDecimal(0, 200)
    tax_rate = factory.fuzzy.FuzzyDecimal(0, 10)
    total_price = factory.fuzzy.FuzzyDecimal(200, 100000)


# TODO: MAKE THIS SMARTER! SO THE FIELDS DEPEND ON EACH OTHER
class ShippingOptionFactory(factory.Factory):
    class Meta:
        model = ShippingOption
        strategy = factory.BUILD_STRATEGY

    customers_account_number = fake.text(max_nb_chars=15)
    customers_carrier = factory.fuzzy.FuzzyChoice(choices=['ups', 'fedex'])
    ship_when = FuzzyDateString(
        start_date=datetime.date.today() + datetime.timedelta(days=1),
        end_date=datetime.date.today() + datetime.timedelta(days=180),
    )
    shipping_method = factory.fuzzy.FuzzyChoice(
        choices=[
            'early_am_overnight',
            'ground',
            'next_day_air',
            'second_day_air',
            'expedited',
        ]
    )
    type = factory.fuzzy.FuzzyChoice(
        choices=['pickup', 'customers_shipping_account', 'suppliers_shipping_account']
    )


class OrderCustomerFactory(factory.Factory):
    class Meta:
        model = OrderCustomer
        strategy = factory.BUILD_STRATEGY

    business_name = fake.company()
    email = fake.company_email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = FuzzyPhoneNumber()
    phone_ext = FuzzyPhoneExt()


class OrderFactory(factory.Factory):
    class Meta:
        model = Order
        strategy = factory.BUILD_STRATEGY

    billing_info = factory.SubFactory(AddressFactory)
    customer = factory.SubFactory(OrderCustomerFactory)
    number = factory.fuzzy.FuzzyInteger(0, 100000)
    order_items = factory.List(
        [factory.SubFactory(OrderItemFactory) for _ in range(random.randrange(1, 20))]
    )
    payment_details = factory.SubFactory(PaymentDetailsFactory)
    shipping_info = factory.SubFactory(AddressFactory)
    shipping_option = factory.SubFactory(ShippingOptionFactory)
