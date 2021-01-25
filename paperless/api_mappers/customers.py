from paperless.api_mappers import (
    BaseMapper,
)


class AccountMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'name',
            'created',
            'credit_line',
            'erp_code',
            'id',
            'notes',
            'payment_terms',
            'payment_terms_period',
            'phone',
            'phone_ext',
            'purchase_orders_enabled',
            'sold_to_address',
            'tax_exempt',
            'tax_rate',
            'url',
        ]
        boolean_keys = ['purchase_orders_enabled', 'tax_exempt']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        for key in boolean_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['sold_to_address'] = (
            AddressMapper.map(resource['sold_to_address'])
            if resource['sold_to_address']
            else None
        )
        mapped_result['billing_addresses'] = map(
            BillingAddressMapper.map, resource['billing_addresses']
        )
        return mapped_result


class AccountListMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['erp_code', 'id', 'name', 'phone', 'phone_ext']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class AddressInfoMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'address1',
            'address2',
            'business_name',
            'city',
            'country',
            'first_name',
            'last_name',
            'phone',
            'phone_ext',
            'postal_code',
            'state',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class AddressMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['address1', 'address2', 'city', 'country', 'postal_code', 'state']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class BillingAddressMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'address1',
            'address2',
            'city',
            'country',
            'id',
            'postal_code',
            'state',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ContactListMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'account_id',
            'created',
            'email',
            'first_name',
            'id',
            'last_name',
            'phone',
            'phone_ext',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'account_id',
            'created',
            'email',
            'first_name',
            'id',
            'last_name',
            'notes',
            'phone',
            'phone_ext',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['address'] = (
            AddressMapper.map(resource['address']) if resource['address'] else None
        )
        return mapped_result


class FacilityMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['account_id', 'attention', 'created', 'id', 'name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['address'] = (
            AddressMapper.map(resource['address']) if resource['address'] else None
        )
        return mapped_result


class PaymentTermsDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'label', 'period']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result
