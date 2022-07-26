from typing import List, Optional

import attr

from paperless.client import PaperlessClient
from paperless.json_encoders.customers import (
    AccountEncoder,
    AddressEncoder,
    ContactEncoder,
    FacilityEncoder,
    PaymentTermsEncoder,
)
from paperless.manager import BaseManager
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
    erp_code = attr.ib(
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


class BillingAddressManager(BaseManager):
    _base_object = BillingAddress

    def create(self, obj, account_id):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = self._client
        data = obj.to_json()
        resp = client.create_resource(
            self._base_object.construct_post_url(account_id), data=data
        )
        resp_obj = self._base_object.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:
            setattr(obj, key, getattr(resp_obj, key))

    def list(self, account_id, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = self._client
        resource_list = self._base_object.parse_list_response(
            client.get_resource_list(
                self._base_object.construct_list_url(account_id), params=params
            )
        )
        return [self._base_object.from_json(resource) for resource in resource_list]


@attr.s(frozen=False)
class Account(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    PaginatedListMixin,
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
    metadata = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((dict, object))),
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
    def construct_paginated_list_url(cls):
        return 'accounts/public'


class AccountManager(BaseManager):
    _base_object = Account

    def search(self, search_term):
        return self.list(params={'search': search_term})

    def filter(self, erp_code=None, name=None, null_erp_code=False):
        return self.list(
            params={'erp_code': erp_code, 'name': name, 'null_erp_code': null_erp_code}
        )


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
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    PaginatedListMixin,
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
    metadata = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((dict, object))),
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
    def construct_list_url(cls):
        return 'contacts/public'


class ContactManager(BaseManager):
    _base_object = Contact

    def filter(self, account_id=None):
        params = {}
        if account_id is not None:
            params['account_id'] = account_id
        return self.list(params=params)

    def search(self, search_term):
        return self.list(params={'search': search_term})


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


class FacilityManager(BaseManager):
    _base_object = Facility

    def create(self, obj, account_id):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = self._client
        data = obj.to_json()
        resp = client.create_resource(
            self._base_object.construct_post_url(account_id), data=data
        )
        resp_obj = self._base_object.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:
            setattr(obj, key, getattr(resp_obj, key))

    def list(self, account_id, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = self._client
        resource_list = self._base_object.parse_list_response(
            client.get_resource_list(
                self._base_object.construct_list_url(account_id), params=params
            )
        )
        return [self._base_object.from_json(resource) for resource in resource_list]


@attr.s(frozen=False)
class PaymentTerms(
    FromJSONMixin,
    ToJSONMixin,
    ReadMixin,
    UpdateMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
):
    _json_encoder = PaymentTermsEncoder

    period: int = attr.ib(validator=attr.validators.instance_of(int))
    erp_code: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of((str, object)))
    )
    label: str = attr.ib(default=NO_UPDATE, validator=attr.validators.instance_of(str))
    id = attr.ib(
        default=NO_UPDATE, validator=attr.validators.instance_of((int, object))
    )

    @classmethod
    def construct_delete_url(cls):
        return 'customers/public/payment_terms'

    @classmethod
    def construct_get_url(cls):
        return 'customers/public/payment_terms'

    @classmethod
    def construct_patch_url(cls):
        return 'customers/public/payment_terms'

    @classmethod
    def construct_post_url(cls):
        return 'customers/public/payment_terms'

    @classmethod
    def construct_list_url(cls):
        return 'customers/public/payment_terms'


class PaymentTermsManager(BaseManager):
    _base_object = PaymentTerms
