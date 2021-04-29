from typing import Optional

import attr

from paperless.client import PaperlessClient
from paperless.json_encoders.customers import (
    AccountEncoder,
    AddressEncoder,
    ContactEncoder,
    FacilityEncoder,
)
from paperless.mixins import (
    CreateMixin,
    DeleteMixin,
    FromJSONMixin,
    ListMixin,
    PaginatedListMixin,
    ReadMixin,
    ToJSONMixin,
    UpdateMixin,
)

from .address import Address
from .common import Money, Salesperson
from .utils import (
    NO_UPDATE,
    convert_cls,
    convert_iterable,
    optional_convert,
    phone_length_validator,
    tax_rate_validator,
)


@attr.s(frozen=False)
class BillingAddress(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
):
    _json_encoder = AddressEncoder
    address1: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    city: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    country: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    postal_code: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    state: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    address2 = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )

    @classmethod
    def construct_delete_url(cls):
        return 'billing_addresses/public'

    @classmethod
    def construct_get_url(cls):
        return 'billing_addresses/public'

    @classmethod
    def construct_patch_url(cls):
        return 'billing_addresses/public'

    @classmethod
    def construct_post_url(cls, account_id):
        return 'accounts/public/{}/billing_addresses'.format(account_id)

    @classmethod
    def construct_list_url(cls, account_id):
        return 'accounts/public/{}/billing_addresses'.format(account_id)

    def create(self, account_id):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.create_resource(self.construct_post_url(account_id), data=data)
        resp_obj = self.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:
            setattr(self, key, getattr(resp_obj, key))

    @classmethod
    def list(cls, account_id=None, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = PaperlessClient.get_instance()
        resource_list = cls.parse_list_response(
            client.get_resource_list(cls.construct_list_url(account_id), params=params)
        )
        if cls._list_object_representation:
            return [
                cls._list_object_representation.from_json(resource)
                for resource in resource_list
            ]
        else:
            return [cls.from_json(resource) for resource in resource_list]


@attr.s(frozen=False)
class Account(
    FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin, CreateMixin, DeleteMixin
):
    _json_encoder = AccountEncoder

    name: str = attr.ib(validator=attr.validators.instance_of(str))

    # not required for instantiation
    billing_addresses = attr.ib(
        default=[], converter=optional_convert(convert_iterable(BillingAddress))
    )
    created = attr.ib(
        default=NO_UPDATE, validator=(attr.validators.instance_of((str, object)))
    )
    credit_line = attr.ib(
        default=NO_UPDATE,
        converter=optional_convert(Money),
        validator=attr.validators.optional(
            attr.validators.instance_of((Money, object))
        ),
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    erp_code = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    notes = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    phone = attr.ib(
        default=NO_UPDATE, validator=attr.validators.optional(phone_length_validator)
    )
    phone_ext = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    payment_terms = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    payment_terms_period = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((int, object))),
    )
    purchase_orders_enabled = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((bool, object))
    )
    salesperson = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Salesperson))
    )
    sold_to_address = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Address))
    )
    tax_exempt = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((bool, object))
    )
    tax_rate = attr.ib(
        default=NO_UPDATE, validator=attr.validators.optional(tax_rate_validator)
    )
    type = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((str, object))
    )
    url = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )

    @classmethod
    def construct_delete_url(cls):
        return 'accounts/public'

    @classmethod
    def construct_get_url(cls):
        return 'accounts/public'

    @classmethod
    def construct_patch_url(cls):
        return 'accounts/public'

    @classmethod
    def construct_post_url(cls):
        return 'accounts/public'

    @classmethod
    def list(cls):
        return AccountList.list()

    @classmethod
    def filter(cls, erp_code=None):
        return AccountList.filter(erp_code=erp_code)

    @classmethod
    def search(cls, search_term):
        return AccountList.search(search_term)


@attr.s(frozen=False)
class AccountList(FromJSONMixin, PaginatedListMixin):

    erp_code: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    type = attr.ib(validator=attr.validators.instance_of(str))

    @classmethod
    def construct_list_url(cls):
        return 'accounts/public'

    @classmethod
    def filter(cls, erp_code):
        return cls.list(params={'erp_code': erp_code})

    @classmethod
    def search(cls, search_term):
        return cls.list(params={'search': search_term})


@attr.s(frozen=False)
class AddressInfo(FromJSONMixin, ToJSONMixin):

    _json_encoder = AddressEncoder

    address1: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    business_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    city: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    country: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    first_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    last_name: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    postal_code: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    state: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    address2 = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )


@attr.s(frozen=False)
class Contact(
    FromJSONMixin, ToJSONMixin, ReadMixin, UpdateMixin, CreateMixin, DeleteMixin
):
    _json_encoder = ContactEncoder

    account_id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))

    # not required for instantiation
    address = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Address))
    )
    created = attr.ib(
        default=NO_UPDATE, validator=(attr.validators.instance_of((str, object)))
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    notes = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    phone = attr.ib(
        default=NO_UPDATE, validator=attr.validators.optional(phone_length_validator)
    )
    phone_ext = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    salesperson = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Salesperson))
    )

    @classmethod
    def construct_delete_url(cls):
        return 'contacts/public'

    @classmethod
    def construct_get_url(cls):
        return 'contacts/public'

    @classmethod
    def construct_patch_url(cls):
        return 'contacts/public'

    @classmethod
    def construct_post_url(cls):
        return 'contacts/public'

    @classmethod
    def list(cls):
        return ContactList.list()

    @classmethod
    def filter(cls, account_id=None):
        return ContactList.filter(account_id=account_id)

    @classmethod
    def search(cls, search_term):
        return ContactList.search(search_term)


@attr.s(frozen=False)
class ContactList(FromJSONMixin, PaginatedListMixin):

    account_id: Optional[int] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(int))
    )
    created: str = attr.ib(validator=attr.validators.instance_of(str))
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    id: int = attr.ib(validator=attr.validators.instance_of(int))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))
    phone: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )
    phone_ext: str = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

    @classmethod
    def construct_list_url(cls):
        return 'contacts/public'

    @classmethod
    def filter(cls, account_id=None):
        params = {}
        if account_id is not None:
            params['account_id'] = account_id
        return cls.list(params=params)

    @classmethod
    def search(cls, search_term):
        return cls.list(params={'search': search_term})


@attr.s(frozen=False)
class Facility(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    ListMixin,
    DeleteMixin,
):
    _json_encoder = FacilityEncoder

    # not required for instantiation
    name = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    account_id = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((int, object))),
    )
    address = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Address))
    )
    attention = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object))),
    )
    created = attr.ib(
        default=NO_UPDATE, validator=(attr.validators.instance_of((str, object)))
    )
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )
    salesperson = attr.ib(
        default=NO_UPDATE, converter=optional_convert(convert_cls(Salesperson))
    )

    @classmethod
    def construct_delete_url(cls):
        return 'facilities/public'

    @classmethod
    def construct_get_url(cls):
        return 'facilities/public'

    @classmethod
    def construct_patch_url(cls):
        return 'facilities/public'

    @classmethod
    def construct_post_url(cls, account_id):
        return 'accounts/public/{}/facilities'.format(account_id)

    @classmethod
    def construct_list_url(cls, account_id):
        return 'accounts/public/{}/facilities'.format(account_id)

    def create(self, account_id):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.create_resource(self.construct_post_url(account_id), data=data)
        resp_obj = self.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:
            setattr(self, key, getattr(resp_obj, key))

    @classmethod
    def list(cls, account_id=None, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = PaperlessClient.get_instance()
        resource_list = cls.parse_list_response(
            client.get_resource_list(cls.construct_list_url(account_id), params=params)
        )
        if cls._list_object_representation:
            return [
                cls._list_object_representation.from_json(resource)
                for resource in resource_list
            ]
        else:
            return [cls.from_json(resource) for resource in resource_list]
