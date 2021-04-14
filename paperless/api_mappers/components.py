from paperless.api_mappers import BaseMapper


class PurchasedComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['oem_part_number', 'piece_price', 'internal_part_number', 'description']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['properties']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        return mapped_result
