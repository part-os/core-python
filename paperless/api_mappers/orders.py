from paperless.api_mappers import BaseMapper


class ComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['material'] = MaterialMapper.map(resource['material']) if resource['material'] else None
        mapped_result['material_operations'] = map(OperationsMapper.map, resource['material_operations'])
        mapped_result['process'] = ProcessMapper.map(resource['process']) if resource['process'] else None
        mapped_result['shop_operations'] = map(OperationsMapper.map, resource['shop_operations'])
        field_keys = ['id', 'deliver_quantity', 'innate_quantity', 'make_quantity', 'description', 'part_name',
                      'part_number', 'part_uuid', 'revision', 'type']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        list_keys = ['child_ids', 'finishes', 'parent_ids', 'supporting_files']
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        return mapped_result


class AddOnMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['name', 'price', 'quantity']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['components'] = map(ComponentMapper.map, resource['components'])
        field_keys = ['id', 'description', 'expedite_revenue', 'filename', 'lead_days', 'private_notes', 'public_notes',
                      'quantity', 'quantity_outstanding', 'quote_item_id', 'quote_item_type', 'root_component_id',
                      'ships_on', 'total_price', 'unit_price', 'base_price', 'add_on_fees']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['ordered_add_ons'] = map(AddOnMapper.map, resource['ordered_add_ons'])
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


class OrderCompanyMapper(BaseMapper):
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


class OrderMinimumMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {'number': resource['number']}


class CostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'type', 'value']
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


class ShippingOptionMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['customers_account_number', 'customers_carrier', 'shipping_method', 'type']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result