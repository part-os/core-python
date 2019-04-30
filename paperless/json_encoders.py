import json
from typing import List

def select_keys(resource, keys: List[str]):
    return {k: getattr(resource, k, None) for k in keys}


class BaseJSONEncoder(object):
    def encode(self, resource):
        raise NotImplementedError


class AddressEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource):
        address_info_values = select_keys(resource, [
            'business_name',
            'first_name',
            'last_name',
            'phone',
            'phone_ext'
        ])
        address_values = select_keys(resource, [
            'address1',
            'address2',
            'city',
            'postal_code'
        ])
        country = { 'abbr': getattr(resource, 'country', None)}
        state = { 'abbr': getattr(resource, 'state', None)}

        return json.dumps({
            **address_info_values,
            'address': {
                **address_values,
                'country': country,
                'state': state
            }
        })


class BaseContactEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource):
        billing_info = []
        if resource.billing_info is not None:
            billing_info.append(resource.billing_info.to_json())

        shipping_info = []
        if resource.shipping_info is not None:
            shipping_info.append(resource.shipping_info.to_json())

        contact_values = {
            **select_keys(resource, keys=[
                'credit_line',
                'phone',
                'phone_ext',
                'purchase_orders',
                'tax_exempt',
                'tax_rate',
                'url'
            ]),
        }

        return ({
            **contact_values,
            'billing_info': billing_info,
            'shipping_info': shipping_info,
        })


class CustomerContactEncoder(BaseContactEncoder):
    @classmethod
    def encode(cls, resource):
        customer_values = {
            **select_keys(resource, keys=[
                'email',
                'first_name',
                'last_name'
            ])
        }

        return json.dumps({
            **super().encode(resource),
            **customer_values
        })
