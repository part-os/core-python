from decimal import *
from typing import List

#from .objects import Order, OrderMinimum

class BaseMapper(object):
    @classmethod
    def map(resource):
        raise NotImplementedError


#TODO: Make this a version
class OrderDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        # Verision 0.0
        billing_info = {
            'address1': resource['buyer_billing']['address']['address1'],
            'address2': resource['buyer_billing']['address']['address2'],
            'business_name': resource['buyer_billing']['business_name'],
            'city': resource['buyer_billing']['address']['city'],
            'country': resource['buyer_billing']['address']['country']['abbr'] if \
                resource['buyer_billing']['address']['country'] else 'USA',
            'first_name': resource['buyer_billing']['first_name'],
            'last_name': resource['buyer_billing']['last_name'],
            'phone': resource['buyer_billing']['phone'],
            'phone_ext': resource['buyer_billing']['phone_ext'],
            'postal_code': resource['buyer_billing']['address']['postal_code'],
            'state': resource['buyer_billing']['address']['state']['abbr'],
        }

        customer = {
            'business_name': resource['customer']['business_name'],
            'email': resource['customer']['email'],
            'first_name': resource['customer']['first_name'],
            'last_name': resource['customer']['last_name'],
            'phone': resource['customer']['phone'],
            'phone_ext': resource['customer']['phone_ext']
        }

        order_items = map(lambda oi: {
            'description': oi['quote_item']['root_component']['description'],
            'filename': oi['quote_item']['root_component']['part']['filename'],
            'material': (oi['quote_item']['material']['custom_name'] \
                    if oi['quote_item']['material']['custom_name'] \
                    else oi['quote_item']['material']['name']) \
                if oi['quote_item']['material'] else None,
            'operations': map(lambda op: {
                'name': op['name'],
            }, oi['quote_item']['root_component']['operations']),
            'part_number': oi['quote_item']['root_component']['part_number'],
            'price': Decimal(oi['price']),
            'private_notes': oi['quote_item']['private_notes'],
            'public_notes': oi['quote_item']['public_notes'],
            'quantity': oi['quantity'],
            'revision': oi['quote_item']['root_component']['revision'],
            'ships_on': oi['ships_on'],
            'unit_price': Decimal(oi['unit_price']),
        }, resource['order_items'])

        payment_details = {
            'net_payout': Decimal(resource['net_payout']) if resource['net_payout'] else None,
            'payment_type': 'purchase_order' if resource['purchase_token'] else 'credit_card',
            'price': Decimal(resource['price']),
            'purchase_order_number': resource['purchase_token'],
            'shipping_cost': Decimal(resource['shipping_cost']),
            'tax_cost': Decimal(resource['tax_cost']) if Decimal(resource['tax_cost']) > 0 else None,
            'tax_rate': Decimal(str(resource['tax_rate'])) if Decimal(resource['tax_rate']) > 0 else None,
        }

        shipping_info = {
            'address1': resource['buyer_shipping']['address']['address1'],
            'address2': resource['buyer_shipping']['address']['address2'],
            'business_name': resource['buyer_shipping']['business_name'],
            'city': resource['buyer_shipping']['address']['city'],
            'country': resource['buyer_shipping']['address']['country']['abbr'] \
                if resource['buyer_shipping']['address']['country'] else 'USA', # TODO: Apparantely for some old addresses we don't have countries stored? See interpro Order 102. I think its better to default it to null then to let it be blank
            'first_name': resource['buyer_shipping']['first_name'],
            'last_name': resource['buyer_shipping']['last_name'],
            'phone': resource['buyer_shipping']['phone'],
            'phone_ext': resource['buyer_shipping']['phone_ext'],
            'postal_code': resource['buyer_shipping']['address']['postal_code'],
            'state': resource['buyer_shipping']['address']['state']['abbr'],
        }

        shipping_option = {
            'customers_account_number': resource['shipping_option']['customers_account_number'],
            'customers_carrier': resource['shipping_option']['customers_carrier'],
            'ship_when': resource['shipping_option']['ship_when'],
            'shipping_method': resource['shipping_option']['shipping_method'],
            'type': resource['shipping_option']['type'],
        }

        return {
            'billing_info': billing_info,
            'customer': customer,
            'number': resource['number'],
            'order_items': order_items,
            'payment_details': payment_details,
            'shipping_info': shipping_info,
            'shipping_option': shipping_option
        }


class OrderMinimumMapper(BaseMapper):
    @classmethod
    def map(cls, resource) -> List[int]:
        return { 'number': resource['number'] }
        #return [o['number'] for o in resources]


class PaymentTermsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            'id': resource['id'],
            'label': resource['label'],
            'period': resource['period']
        }
