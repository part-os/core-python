import json
from paperless.json_encoders import BaseJSONEncoder, SmartJSONEncoder

class PurchasedComponentsPropertiesEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        for item in resource:
            print(item)
            data[getattr(item, 'key', None)] = getattr(item, 'value', None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data


class PurchasedComponentEncoder(SmartJSONEncoder):
    basic_field_keys = [
        'oem_part_number',
        'piece_price',
        'internal_part_number',
        'description'
    ]

    sub_encoders = [
        ('properties', PurchasedComponentsPropertiesEncoder)
    ]
