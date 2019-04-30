import attr
from decimal import Decimal

from typing import Optional

from paperless.api_mappers import PaymentTermsMapper
from paperless.client import PaperlessClient
from paperless.json_encoders import CustomerContactEncoder
from paperless.mixins import FromJSONMixin, ListMixin, ToDictMixin, ToJSONMixin, UpdateMixin

from .address import Address
from .utils import convert_cls, convert_iterable, phone_length_validator, tax_rate_validator

@attr.s
class PaymentTerms(FromJSONMixin, ListMixin, ToDictMixin, UpdateMixin): #TODO: LIST MIXIN
    _mapper = PaymentTermsMapper

    id: int = attr.ib(validator=(attr.validators.instance_of(int)))
    label: str = attr.ib(validator=(attr.validators.instance_of(str)))
    period: int = attr.ib(attr.validators.optional(validator=(attr.validators.instance_of(int))))

    @classmethod
    def construct_list_url(cls):
        client = PaperlessClient.get_instance()
        return 'customers/groups/{}/payment_terms'.format(client.group_slug)


@attr.s
class BaseContact(FromJSONMixin, UpdateMixin):
    billing_info: Optional[Address] = attr.ib(converter=convert_cls(Address), default=None)
    credit_line: Optional[Decimal] = attr.ib(validator=attr.validators.optional(
        attr.validators.instance_of(Decimal)), default=None)
    id: Optional[int] = attr.ib(validator=attr.validators.optional(
        attr.validators.instance_of(int)), default=None)
    payment_terms_id: Optional[PaymentTerms] = attr.ib(converter=convert_cls(PaymentTerms), default=None)
    phone: Optional[int] = attr.ib(validator=attr.validators.optional(
        [attr.validators.instance_of(int), phone_length_validator]), default=None)
    phone_ext: int = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    purchase_orders: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    shipping_info: Optional[Address] = attr.ib(converter=convert_cls(Address), default=None)
    tax_exempt: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    tax_rate: Decimal = attr.ib(validator=attr.validators.optional([
        attr.validators.instance_of(Decimal), tax_rate_validator]), default=None)
    url: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class CompanyContact(BaseContact):
    business_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)


@attr.s
class CustomerContact(BaseContact, ToJSONMixin):
    _json_encoder = CustomerContactEncoder

    company: Optional[CompanyContact] = attr.ib(converter=convert_cls(PaymentTerms), default=None)
    email: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)
    first_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)
    last_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)

    @classmethod
    def construct_post_url(cls):
        client = PaperlessClient.get_instance()
        return 'customers/groups/{}'.format(client.group_slug)
