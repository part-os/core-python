import attr
from decimal import Decimal
import datetime
import dateutil.parser
from typing import List, Optional

from paperless.api_mappers import QuoteDetailsMapper
from paperless.client import PaperlessClient
from paperless.mixins import FromJSONMixin, ListMixin, ReadMixin, ToDictMixin

from .address import Address
from .common import Money
from .contacts import CustomerContact
from .utils import convert_cls, convert_iterable, optional_convert, phone_length_validator


@attr.s(frozen=True)
class Quote(FromJSONMixin, ListMixin, ReadMixin, ToDictMixin):

    _mapper = QuoteDetailsMapper

    number: int = attr.ib(validator=attr.validators.instance_of(int))
    id: int = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def construct_get_url(cls):
        return 'quotes/public'

    @classmethod
    def construct_get_new_resources_url(cls):
        return 'quotes/public/new_sent'

