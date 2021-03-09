from paperless.api_mappers import BaseMapper


class ProcessMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['id', 'external_name', 'name']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class MaterialMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['id', 'display_name', 'family', 'material_class', 'name']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OperationQuantityMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['price', 'manual_price', 'lead_time', 'manual_lead_time', 'quantity']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class PurchasedComponentPropertyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['name', 'code_name', 'value_type', 'value']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class PurchasedComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = [
            'oem_part_number', 'piece_price', 'internal_part_number', 'description'
        ]
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        properties = []
        for prop in resource.get('properties', []):
            properties.append(PurchasedComponentPropertyMapper.map(prop))
        mapped_result['properties'] = properties
        return mapped_result
