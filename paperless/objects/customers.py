from decimal import Decimal
from typing import Optional, List

import attr

from paperless.api_mappers.customers import PaymentTermsDetailsMapper
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin, CreateMixin
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
