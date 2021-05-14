import json
from paperless.objects.utils import NO_UPDATE
from typing import List, Tuple

class BaseJSONEncoder(object):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        raise NotImplementedError

class SmartJSONEncoder(BaseJSONEncoder):
    basic_field_keys: List[str] = []
    sub_encoders: List[Tuple[str, BaseJSONEncoder]] = []        

    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        for key in cls.basic_field_keys:
            data[key] = getattr(resource, key, None)

        for (key, encoder) in cls.sub_encoders:
            value = getattr(resource, key, None)
            if (value is not None and value is not NO_UPDATE):
                data[key] = encoder.encode(value, False)

        filtered_data = {}
        for key in data:
            if data[key] is not None and data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data
