import attr

from typing import Optional

from paperless.mixins import ToJSONMixin


@attr.s
class Address(ToJSONMixin):
    address1: str = attr.ib(validator=attr.validators.instance_of(str))
    city: str = attr.ib(validator=attr.validators.instance_of(str))
    country: str = attr.ib(validator=attr.validators.in_(['CAN', 'USA']))
    postal_code: str = attr.ib(validator=attr.validators.instance_of(str))
    state: str = attr.ib(validator=attr.validators.instance_of(str))  # TODO: DO I WANT THIS TO BE A SATE OR SHOULD THIS BE INTERNATIONAL?

    # optional fields
    id: Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    attention: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    address2: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    business_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    phone: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    phone_ext: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
