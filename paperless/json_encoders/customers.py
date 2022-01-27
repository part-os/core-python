import json

from paperless.json_encoders import BaseJSONEncoder
from paperless.objects.utils import NO_UPDATE
from .common import SalespersonEncoder


class AccountEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = [
            'credit_line',
            'erp_code',
            'notes',
            'name',
            'payment_terms',
            'payment_terms_period',
            'phone',
            'phone_ext',
            'tax_exempt',
            'tax_rate',
            'type',
            'url',
        ]
        for key in field_keys:
            data[key] = getattr(resource, key, None)
        boolean_keys = ['purchase_orders_enabled', 'tax_exempt']
        for key in boolean_keys:
            data[key] = getattr(resource, key, False)

        credit_line = getattr(resource, 'credit_line', None)
        if credit_line is not None and credit_line is not NO_UPDATE:
            data['credit_line'] = MoneyEncoder.encode(credit_line, json_dumps=False)
        else:
            data['credit_line'] = credit_line

        salesperson = getattr(resource, 'salesperson', None)
        if salesperson is not None and salesperson is not NO_UPDATE:
            data['salesperson'] = SalespersonEncoder.encode(salesperson, json_dumps=False)
        else:
            data['salesperson'] = salesperson

        sold_to_address = getattr(resource, 'sold_to_address', None)
        if sold_to_address is not None and sold_to_address is not NO_UPDATE:
            data['sold_to_address'] = AddressEncoder.encode(
                sold_to_address, json_dumps=False
            )
        else:
            data['sold_to_address'] = sold_to_address

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class AddressEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['address1', 'address2', 'city', 'country', 'postal_code', 'state', 'erp_code']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class AddressInfoEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['business_name', 'first_name', 'last_name', 'phone', 'phone_ext']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        address = getattr(resource, 'address', None)
        if address is not None:
            data['address'] = AddressEncoder.encode(address, json_dumps=False)
        else:
            data['address'] = None

        if json_dumps:
            return json.dumps(data)
        else:
            return data


class ContactEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = [
            'account_id',
            'email',
            'first_name',
            'last_name',
            'notes',
            'phone',
            'phone_ext',
        ]
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        address = getattr(resource, 'address', None)
        if address is not None and address is not NO_UPDATE:
            data['address'] = AddressEncoder.encode(address, json_dumps=False)
        else:
            data['address'] = address

        salesperson = getattr(resource, 'salesperson', None)
        if salesperson is not None and salesperson is not NO_UPDATE:
            data['salesperson'] = SalespersonEncoder.encode(salesperson, json_dumps=False)
        else:
            data['salesperson'] = salesperson

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class CountryEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['abbr', 'name']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data


class FacilityEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['account_id', 'attention', 'name']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        address = getattr(resource, 'address', None)
        if address is not None and address is not NO_UPDATE:
            data['address'] = AddressEncoder.encode(address, json_dumps=False)

        salesperson = getattr(resource, 'salesperson', None)
        if salesperson is not None and salesperson is not NO_UPDATE:
            data['salesperson'] = SalespersonEncoder.encode(salesperson, json_dumps=False)
        else:
            data['salesperson'] = salesperson

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class MoneyEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = float(resource.dollars)
        if json_dumps:
            return json.dumps(data)
        else:
            return data


class PaymentTermsEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['id', 'label', 'period']
        for key in field_keys:
            data[key] = getattr(resource, key, None)
        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]
        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class StateEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['abbr', 'name']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data
