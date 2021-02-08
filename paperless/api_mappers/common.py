from paperless.api_mappers import BaseMapper

class SalespersonMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['first_name', 'last_name', 'email']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result