import attr
from decimal import Decimal
from typing import List, Optional

from paperless.api_mappers import OrderDetailsMapper, OrderMinimumMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin

from .address import Address
from .utils import convert_cls, convert_iterable


@attr.s(frozen=True)
class Operation:
    name = attr.ib()
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    runtime: Optional[Decimal] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    setup_time: Optional[Decimal] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))


@attr.s(frozen=True)
class OrderItem:
    description = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    filename = attr.ib()
    lead_days: int = attr.ib(validator=attr.validators.instance_of(int))
    make_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    material = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    part_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    price: Decimal = attr.ib(validator=attr.validators.instance_of(Decimal))
    private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    public_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    revision: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    ships_on = attr.ib(validator=attr.validators.instance_of(str)) # TODO: ADD date type checking and define this values format
    unit_price: Decimal = attr.ib(validator=attr.validators.instance_of(Decimal))


@attr.s(frozen=True)
class PaymentDetails:
    net_payout: Optional[Decimal] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    payment_type: str = attr.ib(validator=attr.validators.in_(['credit_card', 'purchase_order']))
    price: Optional[Decimal] = attr.ib(validator=attr.validators.instance_of(Decimal))
    purchase_order_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_cost: Decimal = attr.ib(validator=attr.validators.instance_of(Decimal))
    tax_cost: Optional[Decimal] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    tax_rate: Optional[Decimal] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    terms: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class ShippingOption:
    customers_account_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    customers_carrier: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.in_(['ups', 'fedex'])))
    ship_when = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_method = attr.ib(validator=attr.validators.optional(attr.validators.in_(
        ['early_am_overnight', 'ground', 'next_day_air', 'second_day_air', 'expedited'])))
    type: str = attr.ib(validator=attr.validators.optional(attr.validators.in_(
        ['pickup', 'customers_shipping_account', 'suppliers_shipping_account'])))


@attr.s(frozen=True)
class OrderCustomer:
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class OrderMinimum(FromJSONMixin):
    _mapper = OrderMinimumMapper

    number = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class Order(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin):
    _mapper = OrderDetailsMapper
    _list_mapper = OrderMinimumMapper
    _list_object_representation = OrderMinimum

    billing_info: Address = attr.ib(converter=convert_cls(Address))
    customer: OrderCustomer = attr.ib(converter=convert_cls(OrderCustomer))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    order_items: List[OrderItem] = attr.ib(converter=convert_iterable(OrderItem))
    payment_details: PaymentDetails = attr.ib(converter=convert_cls(PaymentDetails))
    shipping_info: Address = attr.ib(converter=convert_cls(Address))
    shipping_option: ShippingOption = attr.ib(converter=convert_cls(ShippingOption))

    @classmethod
    def construct_get_url(cls):
        return 'orders/by_number'

    @classmethod
    def construct_get_params(cls):
        client = PaperlessClient.get_instance()
        return {'group': client.group_slug }

    @classmethod
    def construct_list_url(cls):
        client = PaperlessClient.get_instance()
        return 'orders/groups/{}'.format(client.group_slug)

    @classmethod
    def parse_list_response(cls, results):
        return results['results']
