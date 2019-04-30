import attr

from typing import Optional

from paperless.mixins import ToJSONMixin
from paperless.json_encoders import AddressEncoder

from .utils import phone_length_validator


@attr.s
class Address(ToJSONMixin):
    _json_encoder = AddressEncoder

    city: str = attr.ib(validator=attr.validators.instance_of(str))
    country: str = attr.ib(validator=attr.validators.in_(['CA', 'USA']))
    line1: str = attr.ib(validator=attr.validators.instance_of(str))
    postal_code: str = attr.ib(validator=attr.validators.instance_of(str))
    state: str = attr.ib(validator=attr.validators.instance_of(str))  # TODO: DO I WANT THIS TO BE A SATE OR SHOULD THIS BE INTERNATIONAL?

    #optional fields
    business_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
    first_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    last_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    line2: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    phone: Optional[int] = attr.ib(validator=attr.validators.optional(
        [attr.validators.instance_of(int), phone_length_validator]), default=None)
    phone_ext: int = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)