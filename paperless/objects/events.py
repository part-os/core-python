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
    uuid = attr.ib(validator=attr.validators.instance_of(str))
    related_object_type: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str)),
        default=None,
    )
    related_object: Optional[str] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(str)),
        default=None,
    )

    @classmethod
    def construct_list_url(cls):
        return 'events/public'

    @property
    def created_dt(self):
        return (
            dateutil.parser.parse(self.created)
            if isinstance(self.created, str)
            else None
        )
