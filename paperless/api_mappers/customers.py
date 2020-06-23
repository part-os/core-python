from paperless.api_mappers import BaseMapper


class PaymentTermsDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'label', 'period']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class CountryMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['abbr', 'name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class StateMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['abbr', 'name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class AddressMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['city', 'address1', 'address2', 'postal_code']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['country'] = CountryMapper.map(resource['country'])
        mapped_result['state'] = StateMapper.map(resource['state'])
        return mapped_result


class AddressInfoMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['business_name', 'first_name', 'last_name', 'phone', 'phone_ext']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['address'] = AddressMapper.map(resource['address'])
        return mapped_result


class CompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['business_name', 'created', 'credit_line', 'erp_code', 'id', 'notes',
                      'phone', 'phone_ext', 'slug', 'tax_rate', 'url']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        boolean_keys = ['purchase_orders_enabled', 'tax_exempt']
        for key in boolean_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['billing_info'] = AddressInfoMapper.map(resource['billing_info']) if resource['billing_info'] else None
        mapped_result['payment_terms'] = PaymentTermsDetailsMapper.map(resource['payment_terms']) if resource['payment_terms'] else None
        mapped_result['shipping_info'] = AddressInfoMapper.map(resource['shipping_info']) if resource['shipping_info'] else None
        return mapped_result


class CompanyListMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['business_name', 'erp_code', 'id', 'phone', 'phone_ext', 'slug']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result
