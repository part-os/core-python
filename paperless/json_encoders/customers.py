import json
from typing import List

from paperless.json_encoders import BaseJSONEncoder
from paperless.objects.utils import NO_UPDATE


class PaymentTermsEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['id', 'label', 'period']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data


class MoneyEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = float(resource.dollars)
        if json_dumps:
            return json.dumps(data)
        else:
            return data


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
        
        
class AddressEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['address1', 'address2', 'city', 'country', 'first_name',
                      'last_name', 'phone', 'phone_ext', 'postal_code', 'state']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data


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
        
        
class CompanyEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['business_name', 'credit_line', 'erp_code', 'notes',
                      'payment_terms', 'payment_terms_period', 'phone', 'phone_ext',
                      'tax_rate', 'slug', 'url']
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

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data

class CustomerEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['company_id', 'credit_line', 'email', 'first_name', 'last_name',
                      'notes', 'payment_terms', 'payment_terms_period', 'phone', 'phone_ext',
                      'purchase_orders_enabled', 'salesperson', 'tax_exempt', 'tax_rate', 'url']
        for key in field_keys:
            data[key] = getattr(resource, key, None)
        boolean_keys = ['purchase_orders_enabled', 'tax_exempt']
        for key in boolean_keys:
            data[key] = getattr(resource, key, False)
        credit_line = getattr(resource, 'credit_line', None)
        if credit_line is not None:
            data['credit_line'] = MoneyEncoder.encode(credit_line, json_dumps=False)
        else:
            data['credit_line'] = None

        if json_dumps:
            return json.dumps(data)
        else:
            return data
