from paperless.json_encoders.purchased_components import PurchasedComponentEncoder
from paperless.mixins import (
  FromJSONMixin,
  ListMixin,
  ToJSONMixin,
  ReadMixin,
  UpdateMixin,
  CreateMixin,
  DeleteMixin,
  PaginatedListMixin,
) 
from paperless.objects.utils import convert_iterable
from typing import List, Optional, Union
import attr
from paperless.objects.common import Money

@attr.s(frozen=False)
class PurchasedComponentColumn(FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin, CreateMixin, DeleteMixin, ListMixin):
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    code_name: str = attr.ib(validator=attr.validators.instance_of(str))
    value_type: str = attr.ib(validator=attr.validators.instance_of(str))
    default_string_value: Optional[str] = attr.validators.optional(validator=attr.validators.instance_of(str))
    default_boolean_value: bool = attr.ib(validator=attr.validators.instance_of(bool))
    default_numeric_valye: Optional[int] = attr.validators.optional(validator=attr.validators.instance_of(int))
    position: int = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def construct_delete_url(cls):
        return 'suppliers/public/purchased_component_columns'

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/purchased_component_columns'

    @classmethod
    def construct_list_url(cls):
        return 'suppliers/public/purchased_component_columns'

    @classmethod
    def construct_patch_url(cls):
        return 'suppliers/public/purchased_component_columns'

    @classmethod
    def construct_post_url(cls):
        return 'suppliers/public/purchased_component_columns'


@attr.s(frozen=False)
class PurchasedComponentCustomProperty:
    key: str = attr.ib(validator=attr.validators.instance_of(str))
    value: Optional[Union[str, float, bool]] = attr.ib()

@attr.s(frozen=False)
class PurchasedComponent(FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin, CreateMixin, DeleteMixin, PaginatedListMixin):
    _json_encoder = PurchasedComponentEncoder

    id: int = attr.ib(validator=attr.validators.instance_of(int))
    oem_part_number: str = attr.ib(validator=attr.validators.instance_of(str))
    piece_price: str = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    properties: List[PurchasedComponentCustomProperty] = attr.ib(
        converter=convert_iterable(PurchasedComponentCustomProperty)
    )
    internal_part_number: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    description: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

    def get_property(
        self, code_name: str
    ) -> Optional[Union[str, float, bool]]:
        """
        Return the value of the property with the specified code name or None
        """
        return (
            {pcp.code_name: pcp.value for pcp in self.properties}.get(code_name, None)
        )

    @classmethod
    def construct_delete_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_list_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_patch_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_post_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def search(cls, search_term):
        return cls.list(params={'search': search_term})
