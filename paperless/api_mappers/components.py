from paperless.api_mappers import BaseMapper

class AddOnCostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'type', 'value']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result

class CostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'type', 'value', 'row']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ProcessMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['id', 'external_name', 'name']
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


class OperationsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        costing_variables = map(CostingVariablesMapper.map, resource['costing_variables'])
        quantities = map(OperationQuantityMapper.map, resource['quantities'])
        keys = ['id', 'category', 'cost', 'is_finish', 'is_outside_service', 'name', 'operation_definition_name', 'notes', 'position', 'runtime', 'setup_time']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['costing_variables'] = costing_variables
        mapped_result['quantities'] = quantities
        return mapped_result


class MaterialMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['id', 'display_name', 'family', 'material_class', 'name']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result
