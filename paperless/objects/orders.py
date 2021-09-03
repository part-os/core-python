import datetime
from decimal import Decimal
from typing import List, Optional, Union

import attr
import dateutil.parser

from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin, UpdateMixin, ToJSONMixin
from paperless.objects.components import BaseOperation
from paperless.objects.utils import NO_UPDATE

from .address import AddressInfo
from .common import Money, Salesperson
from .components import AssemblyMixin, BaseComponent
from .utils import convert_cls, convert_iterable, optional_convert
from paperless.json_encoders.orders import OrderEncoder

DATE_FMT = '%Y-%m-%d'


@attr.s(frozen=False)
class OrderCostingVariable:
    label: str = attr.ib(validator=attr.validators.instance_of(str))
    value = attr.ib()
    # Note: The row field will only be not None if variable_class == 'table', in which case it will be a dict with
    # arbitrary keys and values
    row: Optional[dict] = attr.ib()
    # Note: The options field will only be not None if variable_class == 'drop_down'
    options: Optional[List[Union[int, float, str]]] = attr.ib()
    variable_class: str = attr.ib(attr.validators.instance_of(str))
    value_type: str = attr.ib(attr.validators.instance_of(str))


@attr.s(frozen=False)
class OrderOperation(BaseOperation):
    costing_variables: List[OrderCostingVariable] = attr.ib(
        converter=convert_iterable(OrderCostingVariable)
    )

    def get_variable(self, label) -> Optional[Union[float, int, str, bool]]:
        """Return the value of the variable with the specified label or None if that variable does not exist."""
        return {cv.label: cv.value for cv in self.costing_variables}.get(label, None)

    def get_variable_obj(self, label) -> Optional[OrderCostingVariable]:
        """Return the value of the variable object with the specified label or None if that variable does not exist."""
        return {cv.label: cv for cv in self.costing_variables}.get(label, None)


@attr.s(frozen=False)
class OrderComponent(BaseComponent):
    deliver_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    make_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    material_operations: List[OrderOperation] = attr.ib(
        converter=convert_iterable(OrderOperation)
    )
    shop_operations: List[OrderOperation] = attr.ib(
        converter=convert_iterable(OrderOperation)
    )


@attr.s(frozen=False)
class OrderedAddOn:
    is_required: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    costing_variables: List[OrderCostingVariable] = attr.ib(
        converter=convert_iterable(OrderCostingVariable)
    )

    def get_variable(self, label) -> Optional[OrderCostingVariable]:
        """Return the value of the variable object with the specified label or None if that variable does not exist."""
        return {cv.label: cv for cv in self.costing_variables}.get(label, None)


@attr.s(frozen=False)
class OrderItem(AssemblyMixin):
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    components: List[OrderComponent] = attr.ib(
        converter=convert_iterable(OrderComponent)
    )
    description: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    expedite_revenue: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(int))
    filename: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    lead_days: int = attr.ib(validator=attr.validators.instance_of(int))
    markup_1_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    markup_1_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    markup_2_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    markup_2_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    private_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    public_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity_outstanding: int = attr.ib(validator=attr.validators.instance_of(int))
    quote_item_id: int = attr.ib(validator=attr.validators.instance_of(int))
    quote_item_type: str = attr.ib(validator=attr.validators.instance_of(str))
    root_component_id: int = attr.ib(validator=attr.validators.instance_of(int))
    ships_on = attr.ib(validator=attr.validators.instance_of(str))
    total_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    unit_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    base_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    add_on_fees: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    ordered_add_ons: List[OrderedAddOn] = attr.ib(
        converter=convert_iterable(OrderedAddOn)
    )

    @property
    def ships_on_dt(self):
        return datetime.datetime.strptime(self.ships_on, DATE_FMT)

    @property
    def root_component(self):
        try:
            return [c for c in self.components if c.is_root_component][0]
        except IndexError:
            raise ValueError('Order item has no root component')

    def get_component(self, component_id: int) -> OrderComponent:
        for component in self.components:
            if component.id == component_id:
                return component


@attr.s(frozen=False)
class PaymentDetails:
    card_brand: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    card_last4: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    net_payout: Money = attr.ib(
        converter=Money,
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    payment_terms: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    payment_type: Optional[str] = attr.ib(
        validator=attr.validators.optional(
            attr.validators.in_(['credit_card', 'purchase_order'])
        )
    )
    purchase_order_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    purchasing_dept_contact_email: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    purchasing_dept_contact_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    shipping_cost: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    subtotal: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    tax_cost: Money = attr.ib(
        converter=Money,
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    tax_rate: Optional[Decimal] = attr.ib(
        converter=optional_convert(Decimal),
        validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
    )
    total_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )


@attr.s(frozen=False)
class ShippingOption:
    customers_account_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    customers_carrier: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.in_(['ups', 'fedex']))
    )
    shipping_method = attr.ib(
        validator=attr.validators.optional(
            attr.validators.in_(
                [
                    'early_am_overnight',
                    'ground',
                    'next_day_air',
                    'second_day_air',
                    'expedited',
                ]
            )
        )
    )
    type: str = attr.ib(
        validator=attr.validators.optional(
            attr.validators.in_(
                ['pickup', 'customers_shipping_account', 'suppliers_shipping_account']
            )
        )
    )

    def summary(self, ships_on_dt, payment_type):
        if self.type == 'pickup':
            return (
                'Customer will pickup from supplier\'s location.\r\n'
                'Deadline: Order should be ready for pickup by start of day '
                '{}.'.format(ships_on_dt.strftime('%m/%d/%Y'))
            )
        elif self.type == 'customers_shipping_account':
            return (
                'Use Customer\'s Shipping Account\r\n'
                'Carrier: {}\r\n'
                'Method: {}\r\n'
                'Account #: {}\r\n'
                'Deadline: Order should ship by noon on {}.'.format(
                    self.customers_carrier.upper(),
                    self.shipping_method.upper(),
                    self.customers_account_number,
                    ships_on_dt.strftime('%m/%d/%Y'),
                )
            )
        elif (self.type == 'suppliers_shipping_account') and (
            payment_type == 'credit_card'
        ):
            return (
                'Customer has been charged for shipping. '
                'Ship with your account.\r\n'
                'Method: {}\r\n'
                'Deadline: Order should ship by noon on {}.'.format(
                    self.shipping_method.upper(), ships_on_dt.strftime('%m/%d/%Y')
                )
            )
        elif (self.type == 'suppliers_shipping_account') and (
            payment_type == 'purchase_order'
        ):
            return (
                'Ship with your account and bill customer for shipping.\r\n'
                'Method: {}\r\n'
                'Deadline: Order should ship by noon on {}.'.format(
                    self.shipping_method.upper(), ships_on_dt.strftime('%m/%d/%Y')
                )
            )


@attr.s(frozen=False)
class ShipmentItem:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    order_item_id: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=False)
class OrderShipment:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    pickup_recipient: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    shipment_date = attr.ib(validator=attr.validators.instance_of(str))
    shipment_items: List[ShipmentItem] = attr.ib(
        converter=convert_iterable(ShipmentItem)
    )
    shipping_cost: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    tracking_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class OrderCompany:
    id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class OrderCustomer:
    id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    company: Optional[OrderCompany] = attr.ib(
        converter=optional_convert(convert_cls(OrderCompany)),
        validator=attr.validators.optional(attr.validators.instance_of(OrderCompany)),
    )
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class OrderAccount:
    id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    payment_terms: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    payment_terms_period: int = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )


@attr.s(frozen=False)
class OrderContact:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    account: OrderAccount = attr.ib(converter=convert_cls(OrderAccount))
    phone: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class OrderMinimum(FromJSONMixin):
    number = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=False)
class Order(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin, UpdateMixin, ToJSONMixin):
    _list_object_representation = OrderMinimum

    _primary_key = 'number'
    _json_encoder = OrderEncoder

    billing_info: AddressInfo = attr.ib(converter=convert_cls(AddressInfo))
    created = attr.ib(validator=attr.validators.instance_of(str))
    contact: OrderContact = attr.ib(converter=convert_cls(OrderContact))
    customer: OrderCustomer = attr.ib(converter=convert_cls(OrderCustomer))
    deliver_by: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    estimator: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    order_items: List[OrderItem] = attr.ib(converter=convert_iterable(OrderItem))
    payment_details: PaymentDetails = attr.ib(converter=convert_cls(PaymentDetails))
    private_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    quote_number: int = attr.ib(validator=attr.validators.instance_of(int))
    sales_person: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    salesperson: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    quote_revision_number: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    shipments: List[OrderShipment] = attr.ib(converter=convert_iterable(OrderShipment))
    shipping_info: AddressInfo = attr.ib(converter=convert_cls(AddressInfo))
    shipping_option: ShippingOption = attr.ib(converter=convert_cls(ShippingOption))
    ships_on = attr.ib(validator=attr.validators.instance_of(str))
    status: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    erp_code = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    quote_erp_code = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )

    @property
    def created_dt(self):
        return dateutil.parser.parse(self.created)

    @property
    def ships_on_dt(self):
        return datetime.datetime.strptime(self.ships_on, DATE_FMT)

    @classmethod
    def construct_get_url(cls):
        return 'orders/public'

    @classmethod
    def construct_list_url(cls):
        client = PaperlessClient.get_instance()
        return 'orders/groups/{}'.format(client.group_slug)

    @classmethod
    def parse_list_response(cls, results):
        return results['results']

    @classmethod
    def construct_patch_url(cls):
        return 'orders/public'
