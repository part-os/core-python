from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.customers import PaymentTermsDetailsMapper, CompanyListMapper, CompanyMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin, CreateMixin, PaginatedListMixin
from .common import Money
from .components import Component, AssemblyMixin
from .utils import convert_cls, optional_convert, convert_iterable, numeric_validator


@attr.s(frozen=True)
class PaymentTerms(FromJSONMixin, ListMixin):

    _mapper = PaymentTermsDetailsMapper

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    label: str = attr.ib(validator=attr.validators.instance_of(str))
    period: int = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def construct_list_url(cls):
        return 'customers/public/payment_terms'


@attr.s(frozen=True)
class Country:
    abbr: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class State:
    abbr: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=True)
class Address:
    country: Country = attr.ib(converter=convert_cls(Country))
    state: State = attr.ib(converter=convert_cls(State))


@attr.s(frozen=True)
class AddressInfo:
    address: Address = attr.ib(converter=convert_cls(Address))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=True)
class CompanyList(FromJSONMixin, PaginatedListMixin):

    _mapper = CompanyListMapper

    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    erp_code: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    phone: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    slug: str = attr.ib(validator=attr.validators.instance_of(str))

    @classmethod
    def construct_list_url(cls):
        return 'companies/public/new'  # TODO - remove the /new

@attr.s(frozen=True)
class Company(FromJSONMixin, ReadMixin):

    _mapper = CompanyMapper

    billing_info: AddressInfo = attr.ib(converter=convert_cls(AddressInfo))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    created: str = attr.ib(validator=attr.validators.instance_of(str))  # TODO - should we convert to datetime?
    credit_line: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    erp_code: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    notes: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    payment_terms: PaymentTerms = attr.ib(converter=convert_cls(PaymentTerms))
    phone: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    purchase_orders_enabled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    shipping_info: AddressInfo = attr.ib(converter=convert_cls(AddressInfo))
    slug: str = attr.ib(validator=attr.validators.instance_of(str))
    tax_exempt: bool = attr.ib(validator=attr.validators.instance_of(bool))
    tax_rate: float = attr.ib(validator=numeric_validator)
    url: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))

    @classmethod
    def construct_get_url(cls):
        return 'companies/public'