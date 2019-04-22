import attr
from decimal import Decimal
from typing import List

def convert_cls(cl):
    """If the attribute is an instance of cls, pass, else try constructing."""
    def converter(val):
        if isinstance(val, cl):
            return val
        else:
            return cl(**val)
    return converter

def convert_iterable(cl):
    # TODO: RAISE UNITERABLE ERROR FOR THIS
    def converter(iterable):
        return [cl(**val) for val in iterable]
    return converter


@attr.s(frozen=True)
class Address:
    business_name = attr.ib(validator=attr.validators.instance_of(str))
    city = attr.ib(validator=attr.validators.instance_of(str))
    country = attr.ib(validator=attr.validators.in_(['CA', 'USA']))
    first_name = attr.ib(validator=attr.validators.instance_of(str))
    last_name = attr.ib(validator=attr.validators.instance_of(str))
    line1 = attr.ib(validator=attr.validators.instance_of(str))
    line2 = attr.ib(validator=attr.validators.instance_of(str))
    phone = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    postal_code = attr.ib(validator=attr.validators.instance_of(str))
    state = attr.ib(validator=attr.validators.instance_of(str))  # TODO: DO I WANT THIS TO BE A SATE OR SHOULD THIS BE INTERNATIONAL?


@attr.s(frozen=True)
class Customer:
    business_name = attr.ib(validator=attr.validators.instance_of(str))
    email = attr.ib(validator=attr.validators.instance_of(str))
    first_name = attr.ib(validator=attr.validators.instance_of(str))
    last_name = attr.ib(validator=attr.validators.instance_of(str))
    phone = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class Operation:
    name = attr.ib()


@attr.s(frozen=True)
class OrderItem:
    description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    filename = attr.ib()
    material= attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    part_number = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    price = attr.ib(validator=attr.validators.instance_of(Decimal))
    private_notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    public_notes = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    quantity = attr.ib(validator=attr.validators.instance_of(int))
    revision = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    ships_on = attr.ib(validator=attr.validators.instance_of(str)) # TODO: ADD date type checking and define this values format
    unit_price = attr.ib(validator=attr.validators.instance_of(Decimal))
    #finishes = attr.ib() #TODO: DO WE NEED THIS?


@attr.s(frozen=True)
class PaymentDetails:
    net_payout = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    payment_type = attr.ib(validator=attr.validators.in_(['credit_card', 'purchase_order']))
    price = attr.ib(validator=attr.validators.instance_of(Decimal))
    purchase_order_number = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_cost = attr.ib(validator=attr.validators.instance_of(Decimal))
    tax_cost = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    tax_rate = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))


@attr.s(frozen=True)
class ShippingOption:
    customers_account_number = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    customers_carrier = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    ship_when = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_method = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    type = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class Order:
    billing_address: Address = attr.ib(converter=convert_cls(Address))
    customer: Customer = attr.ib(converter=convert_cls(Customer))
    number = attr.ib(validator=attr.validators.instance_of(int)) #TODO: TYPING FOR THIS
    order_items: List[OrderItem] = attr.ib(converter=convert_iterable(OrderItem))
    payment_details: PaymentDetails = attr.ib(converter=convert_cls(PaymentDetails)) # TODO: SHOULD THIS BE A DIFFERENT TITLE?
    shipping_address: Address = attr.ib(converter=convert_cls(Address))
    shipping_option: ShippingOption = attr.ib(converter=convert_cls(ShippingOption))


@attr.s(frozen=True)
class OrderMinimum:
    number = attr.ib(validator=attr.validators.instance_of(int))
