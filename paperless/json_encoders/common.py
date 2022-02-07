import json

from paperless.json_encoders import BaseJSONEncoder


class SalespersonEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['email']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        if json_dumps:
            return json.dumps(data)
        else:
            return data
