import json
from typing import List

from paperless.json_encoders import BaseJSONEncoder


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
        field_keys = ['city', 'address1', 'address2', 'postal_code']
        for key in field_keys:
            data[key] = getattr(resource, key, None)
            
        country = getattr(resource, 'country', None)
        if country is not None:
            data['country'] = CountryEncoder.encode(country, json_dumps=False)
        else:
            data['country'] = None
            
        state = getattr(resource, 'state', None)
        if state is not None:
            data['state'] = StateEncoder.encode(state, json_dumps=False)
        else:
            data['state'] = None

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
        field_keys = ['business_name', 'created', 'erp_code', 'id', 'notes',
                      'phone', 'phone_ext', 'slug', 'tax_rate', 'url']
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
            
        billing_info = getattr(resource, 'billing_info', None)
        if billing_info is not None:
            data['billing_info'] = AddressInfoEncoder.encode(billing_info, json_dumps=False)
        else:
            data['bililng_info'] = None

        payment_terms = getattr(resource, 'payment_terms', None)
        if payment_terms is not None:
            data['payment_terms'] = PaymentTermsEncoder.encode(payment_terms, json_dumps=False)
        else:
            data['payment_terms'] = None

        shipping_info = getattr(resource, 'shipping_info', None)
        if shipping_info is not None:
            data['shipping_info'] = AddressInfoEncoder.encode(shipping_info, json_dumps=False)
        else:
            data['bililng_info'] = None

        if json_dumps:
            return json.dumps(data)
        else:
            return data