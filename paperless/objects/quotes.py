from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.quotes import QuoteDetailsMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin
from .common import Money
from .components import Component, AssemblyMixin
from .utils import convert_cls, optional_convert, convert_iterable, numeric_validator


@attr.s(frozen=True)
class AddOnQuantity:
    manual_price: Money = attr.ib(converter=Money, validator=attr.validators.instance_of(Money))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=True)
class AddOn:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    is_required: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    quantities: List[AddOnQuantity] = attr.ib(converter=convert_iterable(AddOnQuantity))


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
class QuoteComponent(Component):
    add_ons: List[AddOn] = attr.ib(converter=convert_iterable(AddOn))
    quantities: List[Quantity] = attr.ib(converter=convert_iterable(Quantity))


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
class QuoteItem(AssemblyMixin):
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    components: List[QuoteComponent] = attr.ib(converter=convert_iterable(QuoteComponent))
    type: str = attr.ib(validator=attr.validators.instance_of(str))
    position: int = attr.ib(validator=attr.validators.instance_of(int))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    component_ids: List[int] = attr.ib(validator=attr.validators.instance_of(list))

    @property
    def root_component(self):
        try:
            return [c for c in self.components if c.is_root_component][0]
        except IndexError:
            raise ValueError('Order item has no root component')

    def get_component(self, component_id: int) -> QuoteComponent:
        for component in self.components:
            if component.id == component_id:
                return component


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
class Quote(FromJSONMixin, ListMixin, ToDictMixin):  # We don't use ReadMixin here because quotes are identified uniquely by (number, revision) pairs

    _mapper = QuoteDetailsMapper

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    sales_person: SalesPerson = attr.ib(converter=convert_cls(SalesPerson))
    estimator: SalesPerson = attr.ib(converter=convert_cls(SalesPerson))
    customer: Customer = attr.ib(converter=convert_cls(Customer))
    tax_rate: Optional[Decimal] = attr.ib(converter=optional_convert(Decimal),
                                          validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    tax_cost: Optional[Money] = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))  # TODO - use optional_convert here
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
    def construct_get_params(cls, revision):
        """
        Optional method to define query params to send along GET request

        :return None or params dict
        """
        return {'revision': revision}

    @classmethod
    def get(cls, id, revision=None):
        """
        Retrieves the resource specified by the id and revision.
        :raise PaperlessNotFoundException: Raised when the requested id 404s aka is not found.
        :param id: int
        :param revision: Optional[int]
        :return: resource
        """
        client = PaperlessClient.get_instance()
        return cls.from_json(client.get_resource(
            cls.construct_get_url(),
            id,
            params=cls.construct_get_params(revision))
        )

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new'

    @classmethod
    def construct_get_new_params(cls, id, revision):
        return {'last_quote': id, 'revision': revision}

    @classmethod
    def get_new(cls, id=None, revision=None):
        client = PaperlessClient.get_instance()

        return client.get_new_resources(
            cls.construct_get_new_resources_url(),
            params=cls.construct_get_new_params(id, revision) if id else None
        )
