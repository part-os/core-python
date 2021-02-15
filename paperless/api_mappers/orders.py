from paperless.api_mappers import BaseMapper
from paperless.api_mappers.components import (
    MaterialMapper,
    OperationQuantityMapper,
    ProcessMapper,
)
from .common import SalespersonMapper


class AddOnMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        costing_variables = map(
            OrderCostingVariablesMapper.map, resource['costing_variables']
        )
        field_keys = ['name', 'notes', 'price', 'quantity']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['is_required']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['costing_variables'] = costing_variables
        return mapped_result


class OrderComponentMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['material'] = (
            MaterialMapper.map(resource['material']) if resource['material'] else None
        )
        mapped_result['material_operations'] = map(
            OrderOperationsMapper.map, resource['material_operations']
        )
        mapped_result['process'] = (
            ProcessMapper.map(resource['process']) if resource['process'] else None
        )
        mapped_result['shop_operations'] = map(
            OrderOperationsMapper.map, resource['shop_operations']
        )
        field_keys = [
            'id',
            'deliver_quantity',
            'innate_quantity',
            'make_quantity',
            'description',
            'part_custom_attrs',
            'part_name',
            'part_number',
            'part_uuid',
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
            'children',
        ]
        for key in list_keys:
            mapped_result[key] = resource.get(key, [])
        bool_keys = ['export_controlled', 'is_root_component']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        return mapped_result


class OrderItemMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['components'] = map(
            OrderComponentMapper.map, resource['components']
        )
        field_keys = [
            'id',
            'description',
            'expedite_revenue',
            'filename',
            'lead_days',
            'private_notes',
            'public_notes',
            'quantity',
            'quantity_outstanding',
            'quote_item_id',
            'quote_item_type',
            'root_component_id',
            'ships_on',
            'total_price',
            'unit_price',
            'base_price',
            'add_on_fees',
            'markup_1_price',
            'markup_1_name',
            'markup_2_price',
            'markup_2_name',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        bool_keys = ['export_controlled']
        for key in bool_keys:
            mapped_result[key] = resource.get(key, False)
        mapped_result['ordered_add_ons'] = map(
            AddOnMapper.map, resource['ordered_add_ons']
        )
        return mapped_result


class OrderAddressInfoMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        if resource is None:
            return None
        mapped_result = {}
        field_keys = [
            'id',
            'attention',
            'address1',
            'address2',
            'business_name',
            'city',
            'country',
            'phone',
            'phone_ext',
            'postal_code',
            'state',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderCompanyMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = ['id', 'business_name', 'erp_code', 'notes']
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderCustomerMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['company'] = (
            OrderCompanyMapper.map(resource['company']) if resource['company'] else None
        )
        field_keys = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'phone_ext',
            'notes',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderAccountMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'id',
            'name',
            'erp_code',
            'notes',
            'payment_terms',
            'payment_terms_period',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderContactMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['account'] = (
            OrderAccountMapper.map(resource['account']) if resource['account'] else None
        )
        field_keys = [
            'id',
            'email',
            'first_name',
            'last_name',
            'notes',
            'phone',
            'phone_ext',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        mapped_result['billing_info'] = OrderAddressInfoMapper.map(
            resource['billing_info']
        )
        mapped_result['contact'] = OrderContactMapper.map(resource['contact'])
        mapped_result['customer'] = OrderCustomerMapper.map(resource['customer'])
        mapped_result['sales_person'] = (
            SalespersonMapper.map(resource['sales_person'])
            if resource['sales_person']
            else None
        )
        mapped_result['salesperson'] = (
            SalespersonMapper.map(resource['salesperson'])
            if resource['salesperson']
            else None
        )
        mapped_result['estimator'] = (
            SalespersonMapper.map(resource['estimator'])
            if resource['estimator']
            else None
        )
        mapped_result['order_items'] = map(OrderItemMapper.map, resource['order_items'])
        mapped_result['payment_details'] = PaymentDetailsMapper.map(
            resource['payment_details']
        )
        mapped_result['shipments'] = map(ShipmentsMapper.map, resource['shipments'])
        mapped_result['shipping_info'] = OrderAddressInfoMapper.map(
            resource['shipping_info']
        )
        mapped_result['shipping_option'] = ShippingOptionMapper.map(
            resource['shipping_option']
        )
        field_keys = [
            'created',
            'deliver_by',
            'number',
            'private_notes',
            'quote_number',
            'quote_revision_number',
            'ships_on',
            'status',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)

        return mapped_result


class OrderMinimumMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        return {'number': resource['number']}


class PaymentDetailsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        mapped_result = {}
        field_keys = [
            'card_brand',
            'card_last4',
            'net_payout',
            'payment_type',
            'purchase_order_number',
            'purchasing_dept_contact_email',
            'purchasing_dept_contact_name',
            'shipping_cost',
            'subtotal',
            'tax_cost',
            'tax_rate',
            'payment_terms',
            'total_price',
        ]
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
        mapped_result['shipment_items'] = map(
            ShipmentItemMapper.map, resource['shipment_items']
        )
        field_keys = [
            'id',
            'pickup_recipient',
            'shipment_date',
            'shipping_cost',
            'tracking_number',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class ShippingOptionMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        if not resource:
            return None
        mapped_result = {}
        field_keys = [
            'customers_account_number',
            'customers_carrier',
            'shipping_method',
            'type',
        ]
        for key in field_keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderCostingVariablesMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        keys = ['label', 'variable_class', 'value_type', 'value', 'row', 'options']
        mapped_result = {}
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        return mapped_result


class OrderOperationsMapper(BaseMapper):
    @classmethod
    def map(cls, resource):
        costing_variables = map(
            OrderCostingVariablesMapper.map, resource['costing_variables']
        )
        quantities = map(OperationQuantityMapper.map, resource['quantities'])
        keys = [
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
        for key in keys:
            mapped_result[key] = resource.get(key, None)
        mapped_result['costing_variables'] = costing_variables
        mapped_result['quantities'] = quantities
        return mapped_result
