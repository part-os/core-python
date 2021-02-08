import json

from paperless.json_encoders import BaseJSONEncoder

class SalespersonEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        if getattr(resource, 'email', False):
            data = { 'email': getattr(resource, 'email') }
        else:
            data = None

        if json_dumps:
            return json.dumps(data)
        else:
            return data