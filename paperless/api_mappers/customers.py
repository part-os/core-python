from paperless.api_mappers import BaseMapper


class PaymentTermsDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'label', 'period']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result
