from decimal import Decimal
from types import SimpleNamespace
from typing import Dict, List, Optional, Union

import attr

from paperless.api_mappers.quotes import QuoteDetailsMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ToDictMixin
from paperless.objects.components import BaseOperation

from .common import Money, Salesperson
from .components import AssemblyMixin, BaseComponent
from .utils import (
    convert_cls,
    convert_dictionary,
    convert_iterable,
    numeric_validator,
    optional_convert,
)


@attr.s(frozen=True)
class CostingVariablePayload:
    value: Optional[Union[float, int, str, bool]] = attr.ib()
    # NOTE: row will only not be None if parent QuoteCostingVariable.variable_class == 'drop_down'
    row: Optional[Dict[str, Union[float, int, str, bool]]] = attr.ib()
    # NOTE: options will only not be None if parent QuoteCostingVariable.variable_class == 'drop_down'
    options: Optional[List[Union[float, int, str]]] = attr.ib()


@attr.s(frozen=True)
class QuoteCostingVariable:
    label: str = attr.ib(validator=attr.validators.instance_of(str))
    quantity_specific: bool = attr.ib()
    quantities: Dict[int, CostingVariablePayload] = attr.ib(
        convert=convert_dictionary(CostingVariablePayload)
    )
    variable_class: str = attr.ib(attr.validators.instance_of(str))
    value_type: str = attr.ib(attr.validators.instance_of(str))


@attr.s(frozen=True)
class QuoteOperation(BaseOperation):
    costing_variables: List[QuoteCostingVariable] = attr.ib(
        converter=convert_iterable(QuoteCostingVariable)
    )

    def get_variable_for_qty(
        self, label: str, qty: int
    ) -> Optional[CostingVariablePayload]:
        """Return the value of the variable with the specified label for the given quantity or None if
        that variable does not exist."""
        return (
            {cv.label: cv.quantities for cv in self.costing_variables}
            .get(label, dict())
            .get(qty, None)
        )

    # TODO: deprecate this
    def get_variable(self, label):
        """Return the value of the variable with the specified label or None if
        that variable does not exist."""
        return {cv.label: cv.value for cv in self.costing_variables}.get(label, None)


@attr.s(frozen=False)
class AddOnQuantity:
    price: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    manual_price: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=False)
class AddOn:
    is_required: bool = attr.ib(validator=attr.validators.instance_of(bool))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    quantities: List[AddOnQuantity] = attr.ib(converter=convert_iterable(AddOnQuantity))
    costing_variables: List[QuoteCostingVariable] = attr.ib(
        converter=convert_iterable(QuoteCostingVariable)
    )

    def get_variable_for_qty(
        self, label: str, qty: int
    ) -> Optional[CostingVariablePayload]:
        """Return the value of the variable with the specified label for the given quantity or None if
        that variable does not exist."""
        return (
            {cv.label: cv.quantities for cv in self.costing_variables}
            .get(label, dict())
            .get(qty, None)
        )


@attr.s(frozen=False)
class Expedite:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    markup: float = attr.ib(validator=numeric_validator)
    unit_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    total_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )


@attr.s(frozen=False)
class Quantity:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    quantity: int = attr.ib(validator=attr.validators.instance_of(int))
    markup_1_price: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    markup_1_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    markup_2_price: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    markup_2_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    unit_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    total_price: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    total_price_with_required_add_ons: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    lead_time: int = attr.ib(validator=attr.validators.instance_of(int))
    expedites: List[Expedite] = attr.ib(converter=convert_iterable(Expedite))
    is_most_likely_won_quantity: bool = attr.ib(validator=attr.validators.instance_of(bool))
    most_likely_won_quantity_percent: int = attr.ib(validator=attr.validators.instance_of(int))


@attr.s(frozen=False)
class QuoteComponent(BaseComponent):
    add_ons: List[AddOn] = attr.ib(converter=convert_iterable(AddOn))
    material_operations: List[QuoteOperation] = attr.ib(
        converter=convert_iterable(QuoteOperation)
    )
    shop_operations: List[QuoteOperation] = attr.ib(
        converter=convert_iterable(QuoteOperation)
    )
    quantities: List[Quantity] = attr.ib(converter=convert_iterable(Quantity))


@attr.s(frozen=False)
class Metrics:
    order_revenue_all_time: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    order_revenue_last_thirty_days: Money = attr.ib(
        converter=Money, validator=attr.validators.instance_of(Money)
    )
    quotes_sent_all_time: int = attr.ib(validator=attr.validators.instance_of(int))
    quotes_sent_last_thirty_days: int = attr.ib(
        validator=attr.validators.instance_of(int)
    )


@attr.s(frozen=False)
class Company:
    id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    metrics: Metrics = attr.ib(converter=convert_cls(Metrics))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class Account:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )


@attr.s(frozen=False)
class Customer:
    id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    company: Company = attr.ib(converter=convert_cls(Company))


@attr.s(frozen=False)
class Contact:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    account: Account = attr.ib(converter=convert_cls(Account))


@attr.s(frozen=False)
class QuoteItem(AssemblyMixin):
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    components: List[QuoteComponent] = attr.ib(
        converter=convert_iterable(QuoteComponent)
    )
    type: str = attr.ib(validator=attr.validators.instance_of(str))
    position: int = attr.ib(validator=attr.validators.instance_of(int))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    component_ids: List[int] = attr.ib(validator=attr.validators.instance_of(list))
    private_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    public_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

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


@attr.s(frozen=False)
class ParentQuote:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    status: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=False)
class ParentSupplierOrder:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    status: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=False)
class RequestForQuote:
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    requested_delivery_date: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    contact_info_conflict: bool = attr.ib(validator=attr.validators.instance_of(bool))


@attr.s(frozen=False)
class Quote(
    FromJSONMixin, ListMixin, ToDictMixin
):  # We don't use ReadMixin here because quotes are identified uniquely by (number, revision) pairs
    STATUSES = SimpleNamespace(
        OUTSTANDING='outstanding', CANCELLED='cancelled', TRASH='trash', LOST='lost'
    )

    _mapper = QuoteDetailsMapper

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    number: int = attr.ib(validator=attr.validators.instance_of(int))
    revision_number: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    sales_person: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    salesperson: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    estimator: Salesperson = attr.ib(converter=convert_cls(Salesperson))
    contact: Contact = attr.ib(converter=convert_cls(Contact))
    customer: Customer = attr.ib(converter=convert_cls(Customer))
    tax_rate: Optional[Decimal] = attr.ib(
        converter=optional_convert(Decimal),
        validator=attr.validators.optional(attr.validators.instance_of(Decimal)),
    )
    tax_cost: Optional[Money] = attr.ib(
        converter=optional_convert(Money),
        validator=attr.validators.optional(attr.validators.instance_of(Money)),
    )
    private_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    quote_items: List[QuoteItem] = attr.ib(converter=convert_iterable(QuoteItem))
    status: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    sent_date: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    expired_date: str = attr.ib(validator=attr.validators.instance_of(str))
    quote_notes: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    digital_last_viewed_on: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    expired: bool = attr.ib(validator=attr.validators.instance_of(bool))
    request_for_quote: Optional[RequestForQuote] = attr.ib(
        converter=convert_cls(RequestForQuote),
        validator=attr.validators.optional(
            attr.validators.instance_of(RequestForQuote)
        ),
    )
    parent_quote: Optional[ParentQuote] = attr.ib(
        converter=convert_cls(ParentQuote),
        validator=attr.validators.optional(attr.validators.instance_of(ParentQuote)),
    )
    parent_supplier_order: Optional[ParentSupplierOrder] = attr.ib(
        converter=convert_cls(ParentSupplierOrder),
        validator=attr.validators.optional(
            attr.validators.instance_of(ParentSupplierOrder)
        ),
    )
    authenticated_pdf_quote_url: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
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
        return cls.from_json(
            client.get_resource(
                cls.construct_get_url(), id, params=cls.construct_get_params(revision)
            )
        )

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new'

    # id is the quote number
    @classmethod
    def construct_get_new_params(cls, id, revision):
        return {'last_quote': id, 'revision': revision}

    # id is the quote number
    @classmethod
    def get_new(cls, id=None, revision=None):
        client = PaperlessClient.get_instance()

        return client.get_new_resources(
            cls.construct_get_new_resources_url(),
            params=cls.construct_get_new_params(id, revision) if id else None,
        )

    def set_status(self, status):
        client = PaperlessClient.get_instance()
        params = None
        if self.revision_number is not None:
            params = {'revision': self.revision_number}
        resp_json = client.request(
            url=f'quotes/public/{self.number}/status_change',
            method=PaperlessClient.METHODS.PATCH,
            data={"status": status},
            params=params,
        )
        resp_obj = self.from_json(resp_json)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:
            setattr(self, key, getattr(resp_obj, key))
