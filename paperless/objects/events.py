from typing import Optional

import attr
import dateutil.parser

from paperless.api_mappers import BaseMapper
from paperless.client import PaperlessClient
from paperless.json_encoders.events import EventEncoder
from paperless.mixins import FromJSONMixin, PaginatedListMixin, ToJSONMixin
from paperless.manager import BaseManager


@attr.s(frozen=False)
class Event(FromJSONMixin, ToJSONMixin, PaginatedListMixin):
    _json_encoder = EventEncoder
    created = attr.ib(validator=attr.validators.instance_of(str))
    data = attr.ib(validator=attr.validators.instance_of(dict))
    type = attr.ib(validator=attr.validators.instance_of(str))
    related_object_type = attr.ib(validator=attr.validators.instance_of(str))
    uuid = attr.ib(validator=attr.validators.instance_of(str))
    related_object: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str))
    )

    @classmethod
    def construct_paginated_list_url(cls):
        return 'events/public/poll'

    @property
    def created_dt(self):
        return (
            dateutil.parser.parse(self.created)
            if isinstance(self.created, str)
            else None
        )

class EventManager(BaseManager):
    _base_object = Event

    def list(self, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :param pages: iterable of ints describing the indices of the pages you want (starting from 1)
        :return: [resource]
        """
        client = self._client
        response = client.get_resource_list(self._base_object.construct_paginated_list_url(), params=params)
        resource_list = self._base_object.parse_list_response(response)
        while response['has_more_events'] is True:
            response = client.get_resource_list(self._base_object.construct_paginated_list_url(), params=params)
            resource_list.extend(self._base_object.parse_list_response(response))
        return [self._base_object.from_json(resource) for resource in resource_list]
