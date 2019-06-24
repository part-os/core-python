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
