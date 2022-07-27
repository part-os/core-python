from typing import Optional

import attr

from paperless.json_encoders.users import UserEncoder
from paperless.manager import (
    BaseManager,
    GetManagerMixin,
    ListManagerMixin,
    UpdateManagerMixin,
)
from paperless.mixins import (
    FromJSONMixin,
    ListMixin,
    ReadMixin,
    ToJSONMixin,
    UpdateMixin,
)


@attr.s(frozen=False)
class User(FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin, ListMixin):
    _primary_key = 'uuid'
    _json_encoder = UserEncoder

    email: str = attr.ib(validator=attr.validators.instance_of(str))
    uuid: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    last_name: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    erp_code: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )

    @classmethod
    def construct_get_url(cls):
        return 'users/public'

    @classmethod
    def construct_list_url(cls):
        return 'users/public'

    @classmethod
    def construct_patch_url(cls):
        return 'users/public'


class UserManager(GetManagerMixin, ListManagerMixin, UpdateManagerMixin, BaseManager):
    _base_object = User
