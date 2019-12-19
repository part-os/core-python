from decimal import Decimal
from typing import Optional

import attr

from paperless.api_mappers import QuoteDetailsMapper
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin
from .common import Money
from .orders import OrderCustomer
from .utils import convert_cls, optional_convert


@attr.s(frozen=True)
class Quote(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin):

    _mapper = QuoteDetailsMapper

    number: int = attr.ib(validator=attr.validators.instance_of(int))
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    tax_cost: Money = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
    tax_rate: Optional[Decimal] = attr.ib(converter=optional_convert(Decimal), validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
    private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    status: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    sent_date: Optional[str] =attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    expired_date: str =attr.ib(validator=attr.validators.instance_of(str))
    quote_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    digital_last_viewed_on: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    expired: bool = attr.ib(validator=attr.validators.instance_of(bool))
    is_unviewed_drafted_rfq: bool = attr.ib(validator=attr.validators.instance_of(bool))
    created: str=attr.ib(validator=attr.validators.instance_of(str))
    authenticated_pdf_quote_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    shipping_cost: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    customer: OrderCustomer = attr.ib(converter=convert_cls(OrderCustomer))
    quote_items = attr.ib()

    @classmethod
    def construct_get_url(cls):
        return 'quotes/public'

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new_sent'

