from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.quotes import QuoteDetailsMapper
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin
from .common import Money
from .orders import OrderCustomer
from .utils import convert_cls, optional_convert, convert_iterable


@attr.s(frozen=True)
class Part:
    filename: str = attr.ib(validator=attr.validators.instance_of(str))
    thumbnail_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    supporting_files: list = attr.ib(validator=attr.validators.instance_of(list))  # TODO - add documentation for supporting_files to the API docs


@attr.s(frozen=True)
class Expedite:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    markup: int = attr.ib(validator=attr.validators.instance_of(int))
    unit_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    total_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))


@attr.s(frozen=True)
class Quantity:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    markup_1_price: Optional[Money] = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    markup_1_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    markup_2_price: Optional[Money] = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    markup_2_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    unit_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    total_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    expedites: List[Expedite] = attr.ib(converter=convert_iterable(Expedite))


@attr.s(frozen=True)
class Operation:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    is_finish: bool = attr.ib(validator=attr.validators.instance_of(bool))


@attr.s(frozen=True)
class Process:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    external_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class Material:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    display_name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Component:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    part: Part = attr.ib(converter=convert_cls(Part))
    part_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    revision: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    description: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    type: str = attr.ib(validator=attr.validators.instance_of(str))
    quantities: List[Quantity] = attr.ib(converter=convert_iterable(Quantity))
    operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    finishes: List = attr.ib(validator=attr.validators.instance_of(list))
    process: Process = attr.ib(converter=convert_cls(Process))
    material: Material = attr.ib(converter=convert_cls(Material))
    material_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class SalesPerson:
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Metric:
    order_revenue_all_time: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    order_revenue_last_thirty_days: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    quotes_sent_all_time: int = attr.ib(validator=attr.validators.instance_of(int))
    quotes_sent_last_thirty_days: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class Company:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    metrics: List[Metric] = attr.ib(converter=convert_iterable(Metric))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Customer:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    company: Company = attr.ib(converter=convert_cls(Company))


@attr.s(frozen=True)
class QuoteItem:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    type: str = attr.ib(validator=attr.validators.instance_of(str))
    root_component: Component = attr.ib(converter=convert_cls(Component))
    position: int = attr.ib(validator=attr.validators.instance_of(int))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    component_ids: List[int] = attr.ib(validator=attr.validators.instance_of(list))


@attr.s(frozen=True)
class Quote(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin):

    _mapper = QuoteDetailsMapper

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    sales_person: SalesPerson = attr.ib(converter=convert_cls(SalesPerson))
    customer: Customer = attr.ib(converter=convert_cls(OrderCustomer))
    tax_rate: Optional[Decimal] = attr.ib(converter=optional_convert(Decimal),
                                          validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    tax_cost: Optional[Money] = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    quote_items: List[QuoteItem] = attr.ib(converter=convert_iterable(QuoteItem))
    status: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    sent_date: Optional[str] =attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    expired_date: str = attr.ib(validator=attr.validators.instance_of(str))
    quote_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    digital_last_viewed_on: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    expired: bool = attr.ib(validator=attr.validators.instance_of(bool))
    request_for_quote: Optional[bool] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)))
    parent_quote: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    parent_supplier_order: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    authenticated_pdf_quote_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    is_unviewed_drafted_rfq: bool = attr.ib(validator=attr.validators.instance_of(bool))
    created: str = attr.ib(validator=attr.validators.instance_of(str))

    @classmethod
    def construct_get_url(cls):
        return 'quotes/public'

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new_sent'
