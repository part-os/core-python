import attr
import types
from typing import Optional
from paperless.client import PaperlessClient
from paperless.mixins import (
    CreateMixin,
    FromJSONMixin,
    ReadMixin,
    ToJSONMixin,
    PaginatedListMixin
)
from paperless.objects.utils import NO_UPDATE
from paperless.json_encoders import BaseJSONEncoder
import json


class IntegrationActionEncoder(BaseJSONEncoder):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        data = {}
        field_keys = ['action_type', 'entity_id', 'status', 'status_message', 'action_uuid']
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


@attr.s(frozen=False)
class IntegrationAction(FromJSONMixin, ToJSONMixin, ReadMixin, CreateMixin, PaginatedListMixin):
    _json_encoder = IntegrationActionEncoder
    action_type = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    entity_id = attr.ib(
        validator=attr.validators.instance_of(str)
    )
    action_uuid: Optional[str] = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object)))
    )
    status: Optional[str] = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.optional(attr.validators.instance_of((str, object)))
    )
    status_message: Optional[str] = attr.ib(
        default=NO_UPDATE,
        validator=attr.validators.instance_of((str, object))
    )

    @classmethod
    def construct_list_url(cls):
        return 'integration_actions/public'

    @classmethod
    def construct_create_url(cls):
        return 'integration_actions/public'

    @classmethod
    def construct_get_url(cls):
        return f'integration_actions/public'

    @classmethod
    def construct_patch_url(cls):
        return f'integration_actions/public'

    @classmethod
    def filter(cls, status: Optional[str] = None, action_type: Optional[str] = None):
        return cls.list(params={'status': status, "action_type": action_type})

    def create(self):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.create_resource(self.construct_create_url(), data=data)
        resp_obj = self.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__') and not x.startswith('_'), dir(resp_obj)
        )
        for key in keys:attr.ib(
            setattr(self, key, getattr(resp_obj, key)))

    def update(self):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.update_resource(
            self.construct_patch_url(), self.action_uuid, data=data
        )
        resp_obj = self.from_json(resp)
        # This filter is designed to remove methods, properties, and private data members and only let through the
        # fields explicitly defined in the class definition
        keys = filter(
            lambda x: not x.startswith('__')
            and not x.startswith('_')
            and type(getattr(resp_obj, x)) != types.MethodType
            and (not isinstance(getattr(resp_obj.__class__, x), property) if x in dir(resp_obj.__class__) else True),
            dir(resp_obj),
        )
        for key in keys:
            setattr(self, key, getattr(resp_obj, key))
