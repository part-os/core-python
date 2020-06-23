from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.customers import PaymentTermsDetailsMapper, CompanyListMapper
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
        return 'companies/public/new'
