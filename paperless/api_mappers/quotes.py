from paperless.api_mappers import BaseMapper
from paperless.api_mappers.components import MaterialMapper, ProcessMapper, OperationQuantityMapper


class QuoteMetricsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['order_revenue_all_time', 'order_revenue_last_thirty_days', 'quotes_sent_all_time',
                      'quotes_sent_last_thirty_days']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteCompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['metrics'] = QuoteMetricsMapper.map(resource['metrics']) if resource['metrics'] else None
        field_keys = ['id', 'business_name', 'erp_code', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteCustomerMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['company'] = QuoteCompanyMapper.map(resource['company']) if resource['company'] else None
        field_keys = ['id', 'email', 'first_name', 'last_name', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteAccountMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'name', 'erp_code', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['account'] = QuoteAccountMapper.map(resource['account']) if resource['account'] else None
        field_keys = ['id', 'email', 'first_name', 'last_name', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteSalesPersonMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['first_name', 'last_name', 'email']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuotePartMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['filename', 'thumbnail_url', 'url']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['supporting_files']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        return mapped_result


class QuoteExpediteMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'lead_time', 'markup', 'unit_price', 'total_price']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteQuantityMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'quantity', 'markup_1_price', 'markup_1_name', 'markup_2_price', 'markup_2_name',
                      'unit_price', 'total_price', 'total_price_with_required_add_ons', 'lead_time']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['expedites'] = map(QuoteExpediteMapper.map, resource['expedites'])
        return mapped_result


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
        keys = ['label', 'variable_class', 'value_type', 'type', 'value', 'row']
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
        costing_variables = map(QuoteCostingVariablesMapper.map, resource['costing_variables'])
        quantities = map(OperationQuantityMapper.map, resource['quantities'])
        keys = ['id', 'category', 'cost', 'is_finish', 'is_outside_service', 'name', 'operation_definition_name', 'notes', 'position', 'runtime', 'setup_time']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['costing_variables'] = costing_variables
        mapped_result['quantities'] = quantities
        return mapped_result


class QuoteOperationQuantityMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['price', 'manual_price', 'lead_time', 'manual_lead_time', 'quantity']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteProcessMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'name', 'external_name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteMaterialMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'name', 'display_name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class AddOnQuantityMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['price', 'manual_price', 'quantity']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class AddOnMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        costing_variables = map(QuoteCostingVariablesMapper.map, resource['costing_variables'])
        field_keys = ['name', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['is_required']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['quantities'] = map(AddOnQuantityMapper.map, resource['quantities'])
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
        mapped_result['components'] = map(QuoteComponentMapper.map,
                                          resource['components'])
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
        field_keys = ['id', 'number', 'revision_number', 'tax_rate', 'tax_cost', 'private_notes', 'status',
                      'sent_date', 'expired_date', 'quote_notes', 'digital_last_viewed_on',
                      'expired', 'authenticated_pdf_quote_url', 'created',
                      'request_for_quote', 'parent_quote', 'parent_supplier_order'
            ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled', 'is_unviewed_drafted_rfq']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['contact'] = QuoteContactMapper.map(resource['contact']) if resource['contact'] else None
        mapped_result['customer'] = QuoteCustomerMapper.map(resource['customer']) if resource['customer'] else None
        mapped_result['sales_person'] = QuoteSalesPersonMapper.map(resource['sales_person']) if resource['sales_person'] else None
        mapped_result['estimator'] = QuoteSalesPersonMapper.map(resource['estimator']) if resource['estimator'] else None
        mapped_result['quote_items'] = map(QuoteItemMapper.map, resource['quote_items'])
        if resource['parent_quote'] is not None:
            mapped_result['parent_quote'] = ParentQuoteMapper.map(resource['parent_quote'])
        if resource['parent_supplier_order'] is not None:
            mapped_result['parent_supplier_order'] = \
                ParentSupplierOrderMapper.map(resource['parent_supplier_order'])
        return mapped_result


class QuoteComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['material'] = MaterialMapper.map(resource['material']) if resource['material'] else None
        mapped_result['material_operations'] = map(QuoteOperationsMapper.map, resource['material_operations'])
        mapped_result['process'] = ProcessMapper.map(resource['process']) if resource['process'] else None
        mapped_result['shop_operations'] = map(QuoteOperationsMapper.map, resource['shop_operations'])
        mapped_result['add_ons'] = map(AddOnMapper.map, resource['add_ons'])
        field_keys = ['id', 'innate_quantity', 'description',
                      'part_custom_attrs', 'part_name', 'part_number',
                      'part_uuid', 'revision', 'thumbnail_url', 'type']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['child_ids', 'finishes', 'parent_ids', 'supporting_files', 'quantities', 'children']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        bool_keys = ['export_controlled', 'is_root_component']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        return mapped_result
