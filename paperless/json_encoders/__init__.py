import json
from typing import List, Tuple

from paperless.objects.utils import NO_UPDATE


class BaseJSONEncoder(object):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        raise NotImplementedError


class SmartJSONEncoder(BaseJSONEncoder):
    """
    JSON Encoder which loops through basic field keys to pick properties.
    Properties are automatically filtered out if the value is NO_UPDATE.
    Pass sub_encoders for complex properties which need their own custom encoder.

    """

    basic_field_keys: List[str] = []
    sub_encoders: List[Tuple[str, BaseJSONEncoder]] = []

    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        for key in cls.basic_field_keys:
            data[key] = getattr(resource, key, None)

        for (key, encoder) in cls.sub_encoders:
            value = getattr(resource, key, NO_UPDATE)
            if value is NO_UPDATE:
                continue
            elif value is None:
                data[key] = None
            else:
                data[key] = encoder.encode(value, False)

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data
