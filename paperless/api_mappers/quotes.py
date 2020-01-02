from paperless.api_mappers import BaseMapper


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
        field_keys = ['id', 'business_name', 'notes']
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
        field_keys = ['filename', 'thumbnail_url', 'url', 'supporting_files']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
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
                      'unit_price', 'total_price', 'lead_time']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['expedites'] = map(QuoteExpediteMapper.map, resource['expedites'])
        return mapped_result


class QuoteOperationMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['is_finish']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
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


class QuoteRootComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'part_number', 'revision', 'description', 'type', 'finishes', 'material_notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['part'] = QuotePartMapper.map(resource['part']) if resource['part'] else None
        mapped_result['quantities'] = map(QuoteQuantityMapper.map, resource['quantities'])
        mapped_result['operations'] = map(QuoteOperationMapper.map, resource['operations'])
        mapped_result['process'] = QuoteProcessMapper.map(resource['process']) if resource['process'] else None
        mapped_result['material'] = QuoteMaterialMapper.map(resource['material']) if resource['material'] else None
        return mapped_result


class QuoteItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'type', 'position', 'component_ids']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['root_component'] = QuoteRootComponentMapper.map(resource['root_component']) if resource['root_component'] else None
        return mapped_result


class QuoteDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'number', 'tax_rate', 'tax_cost', 'private_notes', 'status',
                      'sent_date', 'expired_date', 'quote_notes', 'digital_last_viewed_on',
                      'expired', 'authenticated_pdf_quote_url', 'created',
                      'request_for_quote', 'parent_quote', 'parent_supplier_order'
            ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled', 'is_unviewed_drafted_rfq']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['customer'] = QuoteCustomerMapper.map(resource['customer'])
        mapped_result['sales_person'] = QuoteSalesPersonMapper.map(resource['sales_person'])
        mapped_result['quote_items'] = map(QuoteItemMapper.map, resource['quote_items'])
        return mapped_result
