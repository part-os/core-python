import json
from typing import List

from paperless.json_encoders import BaseJSONEncoder


def select_keys(resource, keys: List[str]):
    return {k: getattr(resource, k, None) for k in keys}


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
            billing_info.append(json.loads(resource.billing_info.to_json()))

        shipping_info = []
        if resource.shipping_info is not None:
            shipping_info.append(json.loads(resource.shipping_info.to_json()))

        payment_terms_id = None
        if resource.payment_terms is not None:
            payment_terms_id = getattr(resource.payment_terms, 'id')

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

        return json.dumps({
            **contact_values,
            'billing_info': billing_info,
            'payment_terms_id': payment_terms_id,
            'shipping_info': shipping_info,
        })


class CustomerContactEncoder(BaseContactEncoder):
    @classmethod
    def encode(cls, resource):
        company_id = None
        if resource.company is not None:
            # TODO: ACCESS PRIMARY KEY?
            company_id = getattr(resource.company, 'id')

        customer_values = {
            **select_keys(resource, keys=[
                'email',
                'first_name',
                'last_name'
            ])
        }

        return json.dumps({
            **json.loads(super().encode(resource)),
            **customer_values,
            'company_id': company_id
        })


class CompanyContactEncoder(BaseContactEncoder):
    @classmethod
    def encode(cls, resource):
        company_values = {
            **select_keys(resource, keys=[
                'business_name',
            ])
        }

        return json.dumps({
            **json.loads(super().encode(resource)),
            **company_values
        })


class PaymentTermsEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource):
        return json.dumps(select_keys(resource, keys=['label','period']))