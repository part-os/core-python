from typing import List, Optional, Union

import attr

from paperless.json_encoders.purchased_components import (
    PurchasedComponentColumnEncoder,
    PurchasedComponentEncoder,
)
from paperless.manager import (
    BaseManager,
    BatchUpsertManagerMixin,
    CreateManagerMixin,
    DeleteManagerMixin,
    GetManagerMixin,
    ListManagerMixin,
    PaginatedListManagerMixin,
    UpdateManagerMixin,
)
from paperless.mixins import (
    BatchMixin,
    CreateMixin,
    DeleteMixin,
    FromJSONMixin,
    ListMixin,
    PaginatedListMixin,
    ReadMixin,
    ToJSONMixin,
    UpdateMixin,
)
from paperless.objects.utils import NO_UPDATE, convert_iterable


@attr.s(frozen=False)
class PurchasedComponentColumn(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
):
    _json_encoder = PurchasedComponentColumnEncoder

    name: str = attr.ib(validator=attr.validators.instance_of(str))
    code_name: str = attr.ib(validator=attr.validators.instance_of(str))
    value_type: str = attr.ib(validator=attr.validators.instance_of(str))
    default_string_value: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    default_boolean_value: bool = attr.ib(validator=attr.validators.instance_of(bool))
    default_numeric_value: Optional[int] = attr.ib()
    id: Union[int, object] = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    position: Union[int, object] = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )

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


class PurchasedComponentColumnManager(
    DeleteManagerMixin,
    GetManagerMixin,
    ListManagerMixin,
    UpdateManagerMixin,
    CreateManagerMixin,
    BaseManager,
):
    _base_object = PurchasedComponentColumn

    def update(self, obj, update_existing_defaults=False):
        self._base_object.update_existing_defaults = update_existing_defaults
        super().update(obj)


@attr.s(frozen=False)
class PurchasedComponentCustomProperty:
    key: str = attr.ib(validator=attr.validators.instance_of(str))
    value: Optional[Union[str, float, bool]] = attr.ib()


@attr.s(frozen=False)
class PurchasedComponent(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    PaginatedListMixin,
    BatchMixin,
):
    _json_encoder = PurchasedComponentEncoder
    _list_key = 'purchased_components'

    oem_part_number: str = attr.ib(validator=attr.validators.instance_of(str))
    piece_price: str = attr.ib(validator=attr.validators.instance_of(str))
    description: Optional[str] = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    internal_part_number: Optional[str] = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    properties: List[PurchasedComponentCustomProperty] = attr.ib(
        default=[], converter=convert_iterable(PurchasedComponentCustomProperty)
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )

    def get_property(self, key: str) -> Optional[Union[str, float, bool]]:
        """
        Return the value of the property with the specified key or None
        """
        val = None
        for pcp in self.properties:
            if pcp.key == key:
                val = pcp.value
        return val

    def set_property(self, key: str, value: Optional[Union[str, float, bool]]):
        """
        Update the value of the property with the specified code name, or add it if it doesn't exist in the list yet
        """
        property = None
        for pcp in self.properties:
            if pcp.key == key:
                property = pcp
        if property is None:
            property = PurchasedComponentCustomProperty(key=key, value=value)
            self.properties.append(property)
        else:
            property.value = value

    @classmethod
    def construct_delete_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_paginated_list_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_patch_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_post_url(cls):
        return 'suppliers/public/purchased_components'

    @classmethod
    def construct_batch_url(cls):
        return f'suppliers/public/purchased_components/batch'


class PurchasedComponentManager(
    DeleteManagerMixin,
    GetManagerMixin,
    PaginatedListManagerMixin,
    UpdateManagerMixin,
    CreateManagerMixin,
    BatchUpsertManagerMixin,
    BaseManager,
):
    _base_object = PurchasedComponent

    def search(self, search_term):
        return self.paginated_list(params={'search': search_term})
