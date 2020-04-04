from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.quotes import QuoteDetailsMapper
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin
from .common import Money
from .utils import convert_cls, optional_convert, convert_iterable, numeric_validator


@attr.s(frozen=True)
class SupportingFile:
    filename: str = attr.ib(validator=attr.validators.instance_of(str))
    url: str = attr.ib(validator=attr.validators.instance_of(str))
    uuid: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=True)
class Part:
    filename: str = attr.ib(validator=attr.validators.instance_of(str))
    thumbnail_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    supporting_files: List[SupportingFile] = attr.ib(converter=convert_iterable(SupportingFile))

@attr.s(frozen=True)
class Expedite:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    markup: float = attr.ib(validator=numeric_validator)
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
    total_price_with_required_add_ons: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    expedites: List[Expedite] = attr.ib(converter=convert_iterable(Expedite))


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
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    external_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class Material:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    display_name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class AddOnQuantity:
    manual_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class AddOn:
    is_required: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    quantities: List[AddOnQuantity] = attr.ib(converter=convert_iterable(AddOnQuantity))


@attr.s(frozen=True)
class Component:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    part: Part = attr.ib(converter=convert_cls(Part))
    part_number: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    revision: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    description: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    type: str = attr.ib(validator=attr.validators.instance_of(str))
    quantities: List[Quantity] = attr.ib(converter=convert_iterable(Quantity))
    shop_operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    material_operations: List[Operation] = attr.ib(converter=convert_iterable(Operation))
    finishes: List = attr.ib(validator=attr.validators.instance_of(list))
    process: Process = attr.ib(converter=convert_cls(Process))
    material: Material = attr.ib(converter=convert_cls(Material))
    material_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    add_ons: List[AddOn] = attr.ib(converter=convert_iterable(AddOn))


@attr.s(frozen=True)
class SalesPerson:
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Metrics:
    order_revenue_all_time: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    order_revenue_last_thirty_days: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    quotes_sent_all_time: int = attr.ib(validator=attr.validators.instance_of(int))
    quotes_sent_last_thirty_days: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class Company:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    metrics: Metrics = attr.ib(converter=convert_cls(Metrics))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class Customer:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
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
class ParentQuote:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    status: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class ParentSupplierOrder:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    status: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Quote(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin):

    _mapper = QuoteDetailsMapper

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    sales_person: SalesPerson = attr.ib(converter=convert_cls(SalesPerson))
    customer: Customer = attr.ib(converter=convert_cls(Customer))
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
    parent_quote: Optional[ParentQuote] = \
        attr.ib(converter=convert_cls(ParentQuote),
                validator=attr.validators.optional(attr.validators.instance_of(ParentQuote)))
    parent_supplier_order: Optional[ParentSupplierOrder] = \
        attr.ib(converter=convert_cls(ParentSupplierOrder),
                validator=attr.validators.optional(attr.validators.instance_of(ParentSupplierOrder)))
    authenticated_pdf_quote_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    is_unviewed_drafted_rfq: bool = attr.ib(validator=attr.validators.instance_of(bool))
    created: str = attr.ib(validator=attr.validators.instance_of(str))

    @classmethod
    def construct_get_url(cls):
        return 'quotes/public'

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new_sent'

    @classmethod
    def construct_get_new_params(cls, id):
        return {'last_quote': id}
