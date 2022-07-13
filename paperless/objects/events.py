from typing import Optional

import attr
import dateutil.parser

from paperless.api_mappers import BaseMapper
from paperless.client import PaperlessClient
from paperless.json_encoders.events import EventEncoder
from paperless.mixins import FromJSONMixin, PaginatedListMixin, ToJSONMixin


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
    def list(cls, params=None, pages=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :param pages: iterable of ints describing the indices of the pages you want (starting from 1)
        :return: [resource]
        """
        client = PaperlessClient.get_instance()
        response = client.get_resource_list(cls.construct_list_url(), params=params)
        resource_list = cls.parse_list_response(response)
        while response['has_more_events'] is True:
            response = client.get_resource_list(cls.construct_list_url(), params=params)
            resource_list.extend(cls.parse_list_response(response))
        if cls._list_object_representation:
            return [
                cls._list_object_representation.from_json(resource)
                for resource in resource_list
            ]
        else:
            return [cls.from_json(resource) for resource in resource_list]

    @classmethod
    def construct_list_url(cls):
        return 'events/public/poll'

    @property
    def created_dt(self):
        return (
            dateutil.parser.parse(self.created)
            if isinstance(self.created, str)
            else None
        )
