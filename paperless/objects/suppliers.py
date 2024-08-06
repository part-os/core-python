import attr

from paperless.json_encoders.suppliers import SupplierFacilityEncoder
from paperless.manager import BaseManager
from paperless.mixins import FromJSONMixin, ToJSONMixin

from .address import Address
from .utils import NO_UPDATE, convert_cls, optional_convert


@attr.s(frozen=False)
class SupplierFacility(FromJSONMixin, ToJSONMixin):
    _json_encoder = SupplierFacilityEncoder

    name = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    address = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Address))
    )
    created = attr.ib(
        default=NO_UPDATE, validator=(attr.validators.instance_of((str, object)))
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    is_default = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((bool, object))
    )
    phone = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    phone_ext = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    url = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )


class SupplierFacilityManager(BaseManager):
    _base_object = SupplierFacility
