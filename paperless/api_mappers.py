from decimal import *

from .objects import Order

class BaseMapper(object):
    @classmethod
    def map(resource):
        raise NotImplementedError


#TODO: Make this a version
class OrderMapper(BaseMapper):

    def map(resource) -> Order:
        # Verision 0.0
        billing_address = {
            'business_name': resource['buyer_billing']['business_name'],
            'city': resource['buyer_billing']['address']['city'],
            'country': resource['buyer_billing']['address']['country']['abbr'],
            'first_name': resource['buyer_billing']['first_name'],
            'last_name': resource['buyer_billing']['last_name'],
            'line1': resource['buyer_billing']['address']['address1'],
            'line2': resource['buyer_billing']['address']['address2'],
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
        }

        order_items = map(lambda oi: {
            'description': oi['quote_item']['root_component']['description'],
            'filename': oi['quote_item']['root_component']['part']['filename'],
            'material': oi['quote_item']['material']['custom_name'] if oi['quote_item']['material']['custom_name'] \
                else oi['quote_item']['material']['name'],
            'operations': map(lambda op: {
                'name': op['name'],
            }, oi['quote_item']['root_component']['operations']),
            'part_number': oi['quote_item']['root_component']['part_number'],
            'price': oi['price'],
            'private_notes': oi['quote_item']['private_notes'],
            'public_notes': oi['quote_item']['public_notes'],
            'quantity': oi['quantity'],
            'revision': oi['quote_item']['root_component']['revision'],
            'ships_on': oi['ships_on'],
            'unit_price': oi['unit_price'],
        }, resource['order_items'])

        payment_details = {
            'net_payout': resource['net_payout'],
            'payment_type': 'purchase_order' if resource['purchase_token'] else 'credit_card',
            'price': resource['price'],
            'purchase_order_number': resource['purchase_token'],
            'shipping_cost': resource['shipping_cost'],
            'tax_cost': resource['tax_cost'] if Decimal(resource['tax_cost']) > 0 else None,
            'tax_rate': resource['tax_rate'] if Decimal(resource['tax_rate']) > 0 else None,
        }

        shipping_address = {
            'business_name': resource['buyer_shipping']['business_name'],
            'city': resource['buyer_shipping']['address']['city'],
            'country': resource['buyer_shipping']['address']['country']['abbr'],
            'first_name': resource['buyer_shipping']['first_name'],
            'last_name': resource['buyer_shipping']['last_name'],
            'line1': resource['buyer_shipping']['address']['address1'],
            'line2': resource['buyer_shipping']['address']['address2'],
            'phone': resource['buyer_shipping']['phone'],
            'phone_ext': resource['buyer_shipping']['phone_ext'],
            'postal_code': resource['buyer_shipping']['address']['postal_code'],
            'state': resource['buyer_shipping']['address']['state']['abbr'],
        }

        return Order(
            billing_address=billing_address,
            customer=customer,
            number=resource['number'],
            order_items=order_items,
            payment_details=payment_details,
            shipping_address=shipping_address
        )
