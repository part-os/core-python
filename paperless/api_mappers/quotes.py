from paperless.api_mappers import BaseMapper


class CostingVariablePayloadMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['value', 'row', 'options']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteCostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'variable_class', 'value_type']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['quantity_specific'] = resource.get('quantity_specific', False)
        quantities = dict()
        for string_qty, value in resource.get('quantities', dict()).items():
            quantities[int(string_qty)] = CostingVariablePayloadMapper.map(value)
        mapped_result['quantities'] = quantities
        return mapped_result


class QuoteOperationsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        costing_variables = map(
            QuoteCostingVariablesMapper.map, resource['costing_variables']
        )
        field_keys = [
            'id',
            'category',
            'cost',
            'is_finish',
            'is_outside_service',
            'name',
            'operation_definition_name',
            'notes',
            'position',
            'runtime',
            'setup_time',
        ]
        mapped_result = {}
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['quantities']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        mapped_result['costing_variables'] = costing_variables
        return mapped_result


class AddOnMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        costing_variables = map(
            QuoteCostingVariablesMapper.map, resource['costing_variables']
        )
        field_keys = ['name', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['is_required']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        list_keys = ['quantities']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        mapped_result['costing_variables'] = costing_variables
        return mapped_result


class QuoteItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'type', 'position', 'private_notes', 'public_notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['component_ids']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['components'] = map(
            QuoteComponentMapper.map, resource['components']
        )
        return mapped_result


class ParentQuoteMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'number', 'status']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ParentSupplierOrderMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'number', 'status']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'id',
            'number',
            'revision_number',
            'tax_rate',
            'tax_cost',
            'private_notes',
            'status',
            'sent_date',
            'expired_date',
            'quote_notes',
            'digital_last_viewed_on',
            'expired',
            'authenticated_pdf_quote_url',
            'created',
            'request_for_quote',
            'parent_quote',
            'parent_supplier_order',
            'estimator',
            'salesperson',
            'sales_person',
            'contact',
            'customer',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled', 'is_unviewed_drafted_rfq']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['quote_items'] = map(QuoteItemMapper.map, resource['quote_items'])
        if resource['parent_quote'] is not None:
            mapped_result['parent_quote'] = ParentQuoteMapper.map(
                resource['parent_quote']
            )
        if resource['parent_supplier_order'] is not None:
            mapped_result['parent_supplier_order'] = ParentSupplierOrderMapper.map(
                resource['parent_supplier_order']
            )
        return mapped_result


class QuoteComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['material_operations'] = map(
            QuoteOperationsMapper.map, resource['material_operations']
        )
        mapped_result['shop_operations'] = map(
            QuoteOperationsMapper.map, resource['shop_operations']
        )
        mapped_result['add_ons'] = map(AddOnMapper.map, resource['add_ons'])
        field_keys = [
            'id',
            'innate_quantity',
            'description',
            'material',
            'part_custom_attrs',
            'part_name',
            'part_number',
            'part_uuid',
            'purchased_component',
            'process',
            'revision',
            'thumbnail_url',
            'type',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = [
            'child_ids',
            'finishes',
            'parent_ids',
            'supporting_files',
            'quantities',
            'children',
        ]
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        bool_keys = ['export_controlled', 'is_root_component']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        return mapped_result
