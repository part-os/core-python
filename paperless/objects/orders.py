import collections
import datetime
from decimal import Decimal
from typing import Generator, List, Optional, NamedTuple

import attr
import dateutil.parser

from paperless.api_mappers.orders import OrderDetailsMapper, OrderMinimumMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin
from .address import Address
from .common import Money
from .utils import convert_cls, convert_iterable, optional_convert

DATE_FMT = '%Y-%m-%d'


@attr.s(frozen=True)
class Material:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    display_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    family: str = attr.ib(validator=attr.validators.instance_of(str))
    material_class: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Operation:
    @attr.s(frozen=True)
    class CostingVariable:
        label: str = attr.ib(validator=attr.validators.instance_of(str))
        type: str = attr.ib(validator=attr.validators.instance_of(str))
        value = attr.ib()

    @attr.s(frozen=True)
    class OperationQuantity:
        price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
        manual_price: Optional[Money] = attr.ib(converter=optional_convert(Money),
                                                validator=attr.validators.optional(attr.validators.instance_of(Money)))
        lead_time: Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
        manual_lead_time: Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
        quantity: int = attr.ib(validator=attr.validators.instance_of(int))

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    category: str = attr.ib(validator=attr.validators.in_(['operation', 'material']))
    cost: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    costing_variables: List[CostingVariable] = attr.ib(converter=convert_iterable(CostingVariable))
    is_finish: bool = attr.ib(validator=attr.validators.instance_of(bool))
    is_outside_service: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    position: int = attr.ib(validator=attr.validators.instance_of(int))
    quantities: List[OperationQuantity] = attr.ib(converter=convert_iterable(OperationQuantity))
    runtime: Optional[float] = attr.ib(converter=optional_convert(float), validator=attr.validators.optional(attr.validators.instance_of(float)))
    setup_time: Optional[float] = attr.ib(converter=optional_convert(float), validator=attr.validators.optional(attr.validators.instance_of(float)))

    def get_variable(self, label):
        """Return the value of the variable with the specified label or None if
        that variable does not exist."""
        return {cv.label: cv.value for cv in self.costing_variables}.get(
            label, None)


@attr.s(frozen=True)
class Process:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    external_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class SupportingFile:
    filename: str = attr.ib(validator=attr.validators.instance_of(str))
    url: str = attr.ib(validator=attr.validators.instance_of(str))
    uuid: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=True)
class Component:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    child_ids: List[int] = attr.ib(converter=convert_iterable(int))
    deliver_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    description: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    finishes: List[str] = attr.ib(converter=convert_iterable(str))
    innate_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    is_root_component: bool = attr.ib(validator=attr.validators.instance_of(bool))
    make_quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    material: Material = attr.ib(converter=convert_cls(Material))
    material_operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    parent_ids: List[int] = attr.ib(converter=convert_iterable(int))
    part_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    part_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    part_uuid: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    process: Process = attr.ib(converter=convert_cls(Process))
    revision: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shop_operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    supporting_files: List[SupportingFile] = attr.ib(converter=convert_iterable(SupportingFile))
    type: str = attr.ib(validator=attr.validators.in_(['assembled', 'manufactured', 'purchased']))


@attr.s(frozen=True)
class AddOn:
    is_required: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


class AssemblyComponent(NamedTuple):
    """A component with metadata describing its position in an assembly.

    Attributes:
        component   the `paperless.objects.orders.Component` instance
        level       this component's depth in the assembly tree (0 is root)
        parent      this component's parent component
        level_index index of this component within its level
        level_count count of components at this assembly level
    """
    component: Component
    level: int  # assembly level (0 for root)
    parent: Optional[Component]
    level_index: int  # 0-based index of the current component within its level
    level_count: int  # count of components at this assembly level


@attr.s(frozen=True)
class OrderItem:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    components: List[Component] = attr.ib(converter=convert_iterable(Component))
    description: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    expedite_revenue: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(int))
    filename: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    lead_days: int = attr.ib(validator=attr.validators.instance_of(int))
    private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    public_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity_outstanding: int = attr.ib(validator=attr.validators.instance_of(int))
    quote_item_id: int = attr.ib(validator=attr.validators.instance_of(int))
    quote_item_type: str = attr.ib(validator=attr.validators.instance_of(str))
    root_component_id: int = attr.ib(validator=attr.validators.instance_of(int))
    ships_on = attr.ib(validator=attr.validators.instance_of(str))
    total_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    unit_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    base_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    add_on_fees: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    ordered_add_ons: List[AddOn] = attr.ib(converter=convert_iterable(AddOn))

    @property
    def ships_on_dt(self):
        return datetime.datetime.strptime(self.ships_on, DATE_FMT)

    @property
    def root_component(self):
        try:
            return [c for c in self.components if c.is_root_component][0]
        except IndexError:
            raise ValueError('Order item has no root component')

    # todo make common after merging quote, order Component into a single class
    def iterate_assembly(self) -> Generator[AssemblyComponent, None, None]:
        """Traverse assembly components in depth-first search ordering.
        Components are yielded as AssemblyComponent (namedtuple) objects,
        containing the component itself as well as information about parent
        and assembly level. The same component will only be yielded once even
        if appears twice in the assembly tree (commonly seen with
        hardware/fasteners)."""
        components_by_id = {}
        root_component = None
        for component in self.components:
            components_by_id[component.id] = component
            if component.is_root_component:
                root_component = component
        level_counter = collections.defaultdict(lambda: 0)
        visited = set()

        def dfs(node_id, level=0, parent=None):
            if node_id in visited:
                return
            visited.add(node_id)
            node = components_by_id[node_id]
            level_index = level_counter[level]
            level_counter[level] += 1
            yield AssemblyComponent(
                component=node,
                level=level,
                parent=parent,
                level_index=level_index,
                level_count=0
            )
            for child_id in node.child_ids:
                for y in dfs(child_id, level + 1, node):
                    yield y

        for assm_comp in list(dfs(root_component.id)):
            yield AssemblyComponent(
                component=assm_comp.component,
                level=assm_comp.level,
                parent=assm_comp.parent,
                level_index=assm_comp.level_index,
                level_count=level_counter[assm_comp.level]
            )


@attr.s(frozen=True)
class PaymentDetails:
    card_brand: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    card_last4: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    net_payout: Money = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    payment_terms: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    payment_type: str = attr.ib(validator=attr.validators.in_(['credit_card', 'purchase_order']))
    purchase_order_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    purchasing_dept_contact_email: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    purchasing_dept_contact_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_cost: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    subtotal: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    tax_cost: Money = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    tax_rate: Optional[Decimal] = attr.ib(converter=optional_convert(Decimal), validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    total_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))


@attr.s(frozen=True)
class ShippingOption:
    customers_account_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    customers_carrier: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.in_(['ups', 'fedex'])))
    shipping_method = attr.ib(validator=attr.validators.optional(attr.validators.in_(
        ['early_am_overnight', 'ground', 'next_day_air', 'second_day_air', 'expedited'])))
    type: str = attr.ib(validator=attr.validators.optional(attr.validators.in_(
        ['pickup', 'customers_shipping_account', 'suppliers_shipping_account'])))

    def summary(self, ships_on_dt, payment_type):
        if self.type == 'pickup':
            return 'Customer will pickup from supplier\'s location.\r\n' \
                   'Deadline: Order should be ready for pickup by start of day ' \
                   '{}.'.format(ships_on_dt.strftime('%m/%d/%Y'))
        elif self.type == 'customers_shipping_account':
            return 'Use Customer\'s Shipping Account\r\n' \
                   'Carrier: {}\r\n' \
                   'Method: {}\r\n' \
                   'Account #: {}\r\n' \
                   'Deadline: Order should ship by noon on {}.'.format(
                self.customers_carrier.upper(),
                self.shipping_method.upper(),
                self.customers_account_number,
                ships_on_dt.strftime('%m/%d/%Y')
            )
        elif (self.type == 'suppliers_shipping_account') and (
                payment_type == 'credit_card'):
            return 'Customer has been charged for shipping. ' \
                   'Ship with your account.\r\n' \
                   'Method: {}\r\n' \
                   'Deadline: Order should ship by noon on {}.'.format(
                self.shipping_method.upper(),
                ships_on_dt.strftime('%m/%d/%Y')
            )
        elif (self.type == 'suppliers_shipping_account') and (
                payment_type == 'purchase_order'):
            return 'Ship with your account and bill customer for shipping.\r\n' \
                   'Method: {}\r\n' \
                   'Deadline: Order should ship by noon on {}.'.format(
                self.shipping_method.upper(),
                ships_on_dt.strftime('%m/%d/%Y')
            )


@attr.s(frozen=True)
class ShipmentItem:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    order_item_id: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class OrderShipment:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    pickup_recipient: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipment_date = attr.ib(validator=attr.validators.instance_of(str))
    shipment_items: List[ShipmentItem] = attr.ib(converter=convert_iterable(ShipmentItem))
    shipping_cost: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    tracking_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class OrderCompany:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class OrderCustomer:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    company: Optional[OrderCompany] = attr.ib(converter=optional_convert(convert_cls(OrderCompany)), validator=attr.validators.optional(attr.validators.instance_of(OrderCompany)))
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
    _list_mapper = OrderMinimumMapper
    _list_object_representation = OrderMinimum
    _mapper = OrderDetailsMapper

    billing_info: Address = attr.ib(converter=convert_cls(Address))
    created = attr.ib(validator=attr.validators.instance_of(str))
    customer: OrderCustomer = attr.ib(converter=convert_cls(OrderCustomer))
    deliver_by: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    order_items: List[OrderItem] = attr.ib(converter=convert_iterable(OrderItem))
    payment_details: PaymentDetails = attr.ib(converter=convert_cls(PaymentDetails))
    private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    quote_number: int = attr.ib(validator=attr.validators.instance_of(int))
    shipments: List[OrderShipment] = attr.ib(converter=convert_iterable(OrderShipment))
    shipping_info: Address = attr.ib(converter=convert_cls(Address))
    shipping_option: ShippingOption = attr.ib(converter=convert_cls(ShippingOption))
    ships_on = attr.ib(validator=attr.validators.instance_of(str))
    status: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))

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
