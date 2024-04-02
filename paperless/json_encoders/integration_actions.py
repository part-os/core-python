import json

from paperless.json_encoders import BaseJSONEncoder, SmartJSONEncoder
from paperless.objects.utils import NO_UPDATE


class IntegrationActionEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['type', 'entity_id', 'status', 'status_message', 'uuid']
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class ManagedIntegrationEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = [
            'erp_name',
            'is_active',
            'erp_version',
            'integration_version',
            'created',
            'updated',
            'configuration_metadata',
        ]
        for key in field_keys:
            data[key] = getattr(resource, key, None)

        filtered_data = {}
        for key in data:
            if data[key] is not NO_UPDATE:
                filtered_data[key] = data[key]

        if json_dumps:
            return json.dumps(filtered_data)
        else:
            return filtered_data


class IntegrationActionErrorEncoder(SmartJSONEncoder):
    basic_field_keys = ['reference_id', 'error_message', 'cause']
