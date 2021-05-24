import json

from paperless.json_encoders import BaseJSONEncoder, SmartJSONEncoder


class PurchasedComponentColumnEncoder(SmartJSONEncoder):
    basic_field_keys = [
        'id',
        'name',
        'code_name',
        'value_type',
        'default_string_value',
        'default_boolean_value',
        'default_numeric_value',
        'position',
        'update_existing_defaults',
    ]


class PurchasedComponentsPropertiesEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        for item in resource:
            data[item.key] = item.value

        if json_dumps:
            return json.dumps(data)
        else:
            return data


class PurchasedComponentEncoder(SmartJSONEncoder):
    basic_field_keys = [
        'oem_part_number',
        'piece_price',
        'internal_part_number',
        'description',
    ]

    sub_encoders = [('properties', PurchasedComponentsPropertiesEncoder)]
