from decimal import Decimal, InvalidOperation


class BaseMapper(object):
    @classmethod
    def map(cls, resource):
        raise NotImplementedError


class AddressMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            'address1': resource['address']['address1'],
            'address2': resource['address']['address2'],
            'business_name': resource['business_name'],
            'city': resource['address']['city'],
            'country': resource['address']['country']['abbr'] if \
                resource['address']['country'] else 'USA',
            'first_name': resource['first_name'],
            'last_name': resource['last_name'],
            'phone': resource['phone'],
            'phone_ext': resource['phone_ext'],
            'postal_code': resource['address']['postal_code'],
            'state': resource['address']['state']['abbr'],
        }


class OperationMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        op = {
            'name': resource['name'],
            'runtime': None,
            'setup_time': None
        }
        for d in resource['display_context']:
            if d.get('secondary_key') == 'runtime':
                try:
                    op['runtime'] = Decimal(d.get('value'))
                except (TypeError, InvalidOperation):
                    pass
            if d.get('secondary_key') == 'setup_time':
                try:
                    op['setup_time'] = Decimal(d.get('value'))
                except (TypeError, InvalidOperation):
                    pass
        try:
            op['runtime'] = Decimal(resource['overrides']['variables']['runtime'])
        except (KeyError, TypeError, InvalidOperation):
            pass
        try:
            op['setup_time'] = Decimal(resource['overrides']['variables']['setup_time'])
        except (KeyError, TypeError, InvalidOperation):
            pass
        return op


class OrderItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        # populate the fields that apply to all quote items
        oi = resource
        d = {
            'price': Decimal(oi['price']),
            'lead_days': oi['lead_time'],
            'private_notes': oi['quote_item']['private_notes'],
            'public_notes': oi['quote_item']['public_notes'],
            'quantity': oi['quantity'],
            'make_quantity': oi['quantity'],
            'ships_on': oi['ships_on'],
            'unit_price': Decimal(oi['unit_price']),
            'description': oi['quote_item']['root_component']['description'],
            'part_number': oi['quote_item']['root_component']['part_number'],
            'revision': oi['quote_item']['root_component']['revision'],
            'filename': oi['quote_item']['root_component']['part']['filename']
                if oi['quote_item']['root_component']['part'] else None,
            'operations': map(
                OperationMapper.map,
                oi['quote_item']['root_component']['operations']),
            'material': None,
        }

        # material for automatic quote items
        if oi['quote_item']['material']:
            d['material'] = oi['quote_item']['material']['custom_name'] \
                if oi['quote_item']['material']['custom_name'] \
                else oi['quote_item']['material']['name']
        # find make qty
        for cq in oi['quote_item']['root_component']['quantities']:
            if cq['quantity'] == oi['quantity']:
                d['make_quantity'] = cq['make_quantity']
                break

        return d


#TODO: Make this a version
class OrderDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        # Version 0.0
        billing_info = AddressMapper.map(resource['buyer_shipping'])

        customer = {
            'business_name': resource['customer']['business_name'],
            'email': resource['customer']['email'],
            'first_name': resource['customer']['first_name'],
            'last_name': resource['customer']['last_name'],
            'phone': resource['customer']['phone'],
            'phone_ext': resource['customer']['phone_ext']
        }

        order_items = map(OrderItemMapper.map, resource['order_items'])

        payment_details = {
            'net_payout': Decimal(resource['net_payout']) if resource['net_payout'] else None,
            'payment_type': 'purchase_order' if resource['purchase_token'] else 'credit_card',
            'price': Decimal(resource['price']),
            'purchase_order_number': resource['purchase_token'],
            'shipping_cost': Decimal(resource['shipping_cost']),
            'tax_cost': Decimal(resource['tax_cost']) if Decimal(resource['tax_cost']) > 0 else None,
            'tax_rate': Decimal(str(resource['tax_rate'])) if Decimal(resource['tax_rate']) > 0 else None,
            'terms': resource.get('payment_terms', dict()).get('label') if resource['purchase_token'] else None,
        }

        shipping_info = AddressMapper.map(resource['buyer_shipping'])

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
    def map(cls, resource):
        return {'number': resource['number']}


class PaymentTermsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            'id': resource['id'],
            'label': resource['label'],
            'period': resource['period']
        }


class BaseContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        # HACK: Billing Info/Shipping Info is a list for some reason... we only ever interact with one on the paperless parts platform so thats all we show.
        return {
            'billing_info': AddressMapper.map(resource['billing_info']) if \
                len(resource['billing_info']) else None,
            'credit_line': resource['credit_line'],
            'id': resource['id'],
            'payment_terms': PaymentTermsMapper.map(resource['payment_terms']) if \
                resource['payment_terms'] else None,
            'phone': resource['phone'],
            'phone_ext': resource['phone_ext'],
            'purchase_orders': resource['purchase_orders'],
            'shipping_info': AddressMapper.map(resource['shipping_info']) if \
                len(resource['shipping_info']) else None,
            'tax_exempt': resource['tax_exempt'],
            'url': resource['url']
        }


class CompanyContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            **BaseContactMapper.map(resource),
            'business_name': resource['business_name']
        }


class CustomerContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            **BaseContactMapper.map(resource),
            'company': CompanyContactMapper.map(resource['company']) if \
                resource['company'] else None,
            'email': resource['email'],
            'first_name': resource['first_name'],
            'last_name': resource['last_name']
        }
