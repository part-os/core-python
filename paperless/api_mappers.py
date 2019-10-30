class BaseMapper(object):
    @classmethod
    def map(cls, resource):
        raise NotImplementedError


class AddressMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            'address1': resource['address']['address1'],
            'address2': resource['address']['address2'],
            'business_name': resource['business_name'],
            'city': resource['address']['city'],
            'country': resource['address']['country']['abbr'] if \
                resource['address']['country'] else 'USA',
            'first_name': resource['first_name'],
            'last_name': resource['last_name'],
            'phone': resource['phone'],
            'phone_ext': resource['phone_ext'],
            'postal_code': resource['address']['postal_code'],
            'state': resource['address']['state']['abbr'],
        }


class OrderMinimumMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {'number': resource['number']}


class PaymentTermsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            'id': resource['id'],
            'label': resource['label'],
            'period': resource['period']
        }


class BaseContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        # HACK: Billing Info/Shipping Info is a list for some reason... we only ever interact with one on the paperless parts platform so thats all we show.
        return {
            'billing_info': AddressMapper.map(resource['billing_info']) if \
                len(resource['billing_info']) else None,
            'credit_line': resource['credit_line'],
            'id': resource['id'],
            'payment_terms': PaymentTermsMapper.map(resource['payment_terms']) if \
                resource['payment_terms'] else None,
            'phone': resource['phone'],
            'phone_ext': resource['phone_ext'],
            'purchase_orders': resource['purchase_orders'],
            'shipping_info': AddressMapper.map(resource['shipping_info']) if \
                len(resource['shipping_info']) else None,
            'tax_exempt': resource['tax_exempt'],
            'url': resource['url']
        }


class CompanyContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            **BaseContactMapper.map(resource),
            'business_name': resource['business_name']
        }


class CustomerContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {
            **BaseContactMapper.map(resource),
            'company': CompanyContactMapper.map(resource['company']) if \
                resource['company'] else None,
            'email': resource['email'],
            'first_name': resource['first_name'],
            'last_name': resource['last_name']
        }


class CostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'type', 'value']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result

class OperationsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        costing_variables = map(CostingVariablesMapper.map, resource['costing_variables'])
        keys = ['id', 'category', 'cost', 'name', 'notes', 'position', 'runtime', 'setup_time']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['is_finish'] = resource.get('is_finish', False)
        mapped_result['costing_variables'] = costing_variables
        return mapped_result

class MaterialMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['id', 'display_name', 'family', 'material_class', 'name']
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

class ComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['material'] = MaterialMapper.map(resource['material']) if resource['material'] else None
        mapped_result['material_operations'] = map(OperationsMapper.map, resource['material_operations'])
        mapped_result['process'] = ProcessMapper.map(resource['process']) if resource['process'] else None
        mapped_result['shop_operations'] = map(OperationsMapper.map, resource['shop_operations'])
        field_keys = ['id', 'deliver_quantity', 'innate_quantity', 'make_quantity', 'description', 'part_name', 'part_number', 'part_uuid', 'revision', 'type']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['child_ids', 'finishes', 'parent_ids']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        return mapped_result

class OrderItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['components'] = map(ComponentMapper.map, resource['components'])
        field_keys = ['id', 'description', 'expedite_revenue', 'filename', 'lead_days', 'private_notes', 'public_notes',
                      'quantity', 'quantity_outstanding', 'quote_item_id', 'quote_item_type', 'root_component_id',
                      'ships_on', 'total_price', 'unit_price']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        return mapped_result


class PaymentDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['card_brand', 'card_last4', 'net_payout', 'payment_type', 'purchase_order_number',
                      'purchasing_dept_contact_email', 'purchasing_dept_contact_name', 'shipping_cost', 'subtotal',
                      'tax_cost', 'tax_rate', 'payment_terms', 'total_price']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ShipmentItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'order_item_id', 'quantity']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ShipmentsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['shipment_items'] = map(ShipmentItemMapper.map, resource['shipment_items'])
        field_keys = ['id', 'pickup_recipient', 'shipment_date', 'shipping_cost', 'tracking_number']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderAddressInfoMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'address1', 'address2', 'business_name', 'city', 'country', 'first_name', 'last_name',
                      'phone', 'phone_ext', 'postal_code', 'state']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ShippingOptionMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['customers_account_number', 'customers_carrier', 'shipping_method', 'type']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderCompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'business_name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result

class QuoteCompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'business_name']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result

class OrderCustomerMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['company'] = OrderCompanyMapper.map(resource['company']) if resource['company'] else None
        field_keys = ['id', 'email', 'first_name', 'last_name', 'phone', 'phone_ext']
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

class OrderDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['billing_info'] = OrderAddressInfoMapper.map(resource['billing_info'])
        mapped_result['customer'] = OrderCustomerMapper.map(resource['customer'])
        mapped_result['order_items'] = map(OrderItemMapper.map, resource['order_items'])
        mapped_result['payment_details'] = PaymentDetailsMapper.map(resource['payment_details'])
        mapped_result['shipments'] = map(ShipmentsMapper.map, resource['shipments'])
        mapped_result['shipping_info'] = OrderAddressInfoMapper.map(resource['shipping_info'])
        mapped_result['shipping_option'] = ShippingOptionMapper.map(resource['shipping_option'])
        field_keys = ['created', 'deliver_by', 'number', 'private_notes', 'quote_number', 'ships_on', 'status']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)

        return mapped_result


class QuoteDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id','digi_quote_key','number','tax_rate','tax_cost',\
                'private_notes','status','sent_date','expired_date','quote_notes','export_controlled','digital_last_viewed_on'\
                ,'expired','authenticated_pdf_quote_url','is_unviewed_drafted_rfq','shipping_cost','created'
            ]
        mapped_result['customer'] = QuoteCustomerMapper.map(resource['customer'])
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result
        # mapped_result['id'] = resource['id']
        # return mapped_result


        # number: int = attr.ib(validator=attr.validators.instance_of(int))
        # id: int = attr.ib(validator=attr.validators.instance_of(int))
        # tax_cost: Money = attr.ib(converter=Money, validator=attr.validators.optional(attr.validators.instance_of(Money)))
        # tax_rate: Optional[Decimal] = attr.ib(converter=optional_convert(Decimal), validator=attr.validators.optional(attr.validators.instance_of(Decimal)))
        # private_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
        # status: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
        # sent_date: str =attr.ib(validator=attr.validators.instance_of(str))
        # expired_date: str =attr.ib(validator=attr.validators.instance_of(str))
        # quote_notes: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
        # export_controlled: bool = attr.ib(validator=attr.validators.instance_of(bool))
        # digital_last_viewed_on: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))
        # expired: bool = attr.ib(validator=attr.validators.instance_of(bool))
        # is_unviewed_drafted_rfq: bool = attr.ib(validator=attr.validators.instance_of(bool))
        # created: str=attr.ib(validator=attr.validators.instance_of(str))
        # authenticated_pdf_quote_url: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)))