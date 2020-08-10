from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.customers import PaymentTermsDetailsMapper, CompanyListMapper, CompanyMapper
from paperless.client import PaperlessClient
from paperless.json_encoders.customers import PaymentTermsEncoder, CompanyEncoder
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin, CreateMixin, PaginatedListMixin, \
    UpdateMixin, ToJSONMixin
from .common import Money
from .components import Component, AssemblyMixin
from .utils import convert_cls, optional_convert, convert_iterable, numeric_validator


@attr.s(frozen=False)
class PaymentTerms(FromJSONMixin, ToJSONMixin, ListMixin):

    _mapper = PaymentTermsDetailsMapper
    _json_encoder = PaymentTermsEncoder

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    label: str = attr.ib(validator=attr.validators.instance_of(str))
    period: Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))

    @classmethod
    def construct_list_url(cls):
        return 'customers/public/payment_terms'


@attr.s(frozen=False)
class Country:
    abbr: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=False)
class State:
    abbr: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.s(frozen=False)
class Address:
    country: Country = attr.ib(converter=convert_cls(Country))
    state: State = attr.ib(converter=convert_cls(State))
    city: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    address1: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    address2: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    postal_code: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=False)
class AddressInfo:
    address: Address = attr.ib(converter=convert_cls(Address))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))


@attr.s(frozen=False)
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
        return 'companies/public'


@attr.s(frozen=False)
class Company(FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin):

    _mapper = CompanyMapper
    _json_encoder = CompanyEncoder

    billing_info: Optional[AddressInfo] = attr.ib(converter=optional_convert(convert_cls(AddressInfo)))
    business_name: str = attr.ib(validator=attr.validators.instance_of(str))
    created: str = attr.ib(validator=attr.validators.instance_of(str))
    credit_line: Optional[Money] = attr.ib(converter=optional_convert(Money), validator=attr.validators.optional(attr.validators.instance_of(Money)))
    erp_code: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    payment_terms: Optional[PaymentTerms] = attr.ib(converter=optional_convert(convert_cls(PaymentTerms)))
    phone: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    phone_ext: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    purchase_orders_enabled: bool = attr.ib(validator=attr.validators.instance_of(bool))
    shipping_info: Optional[AddressInfo] = attr.ib(converter=optional_convert(convert_cls(AddressInfo)))
    slug: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    tax_exempt: bool = attr.ib(validator=attr.validators.instance_of(bool))
    tax_rate: Optional[float] = attr.ib(validator=attr.validators.optional(numeric_validator))
    url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))

    @classmethod
    def construct_get_url(cls):
        return 'companies/public'

    def construct_patch_url(cls):
        return 'companies/public'
