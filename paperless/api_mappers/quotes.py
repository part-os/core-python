from paperless.api_mappers import BaseMapper


class QuoteCompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'business_name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteCustomerMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['company'] = QuoteCompanyMapper.map(resource['company']) if resource['company'] else None
        field_keys = ['id', 'email', 'first_name', 'last_name', 'phone', 'phone_ext']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class QuoteDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'number', 'tax_rate', 'tax_cost', 'quote_items', 'private_notes', 'status',
                      'sent_date', 'expired_date', 'quote_notes', 'export_controlled', 'digital_last_viewed_on',
                      'expired', 'authenticated_pdf_quote_url', 'is_unviewed_drafted_rfq', 'created',
                      'sales_person', 'request_for_quote', 'parent_quote', 'parent_supplier_order'
            ]
        mapped_result['customer'] = QuoteCustomerMapper.map(resource['customer'])
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result