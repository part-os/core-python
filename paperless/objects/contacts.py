import attr
from decimal import Decimal

from typing import Optional

from paperless.api_mappers import CompanyContactMapper, CustomerContactMapper, PaymentTermsMapper
from paperless.client import PaperlessClient
from paperless.json_encoders import CompanyContactEncoder, CustomerContactEncoder, PaymentTermsEncoder
from paperless.mixins import CreateMixin, FromJSONMixin, ListMixin, ToDictMixin, ToJSONMixin, UpdateMixin

from .address import Address
from .utils import convert_cls, phone_length_validator, tax_rate_validator


@attr.s
class PaymentTerms(CreateMixin, FromJSONMixin, ListMixin, ToDictMixin, ToJSONMixin):
    _mapper = PaymentTermsMapper
    _json_encoder = PaymentTermsEncoder

    id: int = attr.ib(validator=(attr.validators.instance_of(int)))
    label: str = attr.ib(validator=(attr.validators.instance_of(str)))
    period: int = attr.ib(attr.validators.optional(validator=(attr.validators.instance_of(int))))

    @classmethod
    def construct_list_url(cls):
        client = PaperlessClient.get_instance()
        return 'customers/groups/{}/payment_terms'.format(client.group_slug)

    @classmethod
    def construct_post_url(cls):
        client = PaperlessClient.get_instance()
        return 'customers/groups/{}/payment_terms'.format(client.group_slug)


@attr.s
class BaseContact(CreateMixin, FromJSONMixin, ToJSONMixin, UpdateMixin):
    billing_info: Optional[Address] = attr.ib(converter=convert_cls(Address), default=None)
    credit_line: Optional[Decimal] = attr.ib(validator=attr.validators.optional(
        attr.validators.instance_of(Decimal)), default=None)
    id: Optional[int] = attr.ib(validator=attr.validators.optional(
        attr.validators.instance_of(int)), default=None)
    payment_terms: Optional[PaymentTerms] = attr.ib(converter=convert_cls(PaymentTerms), default=None)
    phone: Optional[str] = attr.ib(validator=attr.validators.optional(
        [attr.validators.instance_of(str), phone_length_validator]), default=None)
    phone_ext: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    purchase_orders: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    shipping_info: Optional[Address] = attr.ib(converter=convert_cls(Address), default=None)
    tax_exempt: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    tax_rate: Decimal = attr.ib(validator=attr.validators.optional([
        attr.validators.instance_of(Decimal), tax_rate_validator]), default=None)
    url: str = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)


@attr.s
class CompanyContact(BaseContact):
    _json_encoder = CompanyContactEncoder
    _mapper = CompanyContactMapper

    business_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)

    @classmethod
    def construct_patch_url(cls):
        return 'companies'

    @classmethod
    def construct_post_url(cls):
        client = PaperlessClient.get_instance()
        return 'companies/groups/{}'.format(client.group_slug)


@attr.s
class CustomerContact(BaseContact):
    _json_encoder = CustomerContactEncoder
    _mapper = CustomerContactMapper

    company: Optional[CompanyContact] = attr.ib(converter=convert_cls(CompanyContact), default=None)
    email: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)
    first_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)
    last_name: str = attr.ib(validator=attr.validators.instance_of(str), kw_only=True)

    @classmethod
    def construct_patch_url(cls):
        return 'customers'

    @classmethod
    def construct_post_url(cls):
        client = PaperlessClient.get_instance()
        return 'customers/groups/{}'.format(client.group_slug)
