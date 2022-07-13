from tokenize import Number
from typing import Optional

import attr

from paperless.client import PaperlessClient
from paperless.json_encoders.integration_heartbeats import IntegrationHeartbeatEncoder
from paperless.mixins import CreateMixin, ToJSONMixin


@attr.s(frozen=False)
class IntegrationHeartbeat(ToJSONMixin, CreateMixin):
    _json_encoder = IntegrationHeartbeatEncoder
    interval = attr.ib(validator=attr.validators.instance_of(int))

    @classmethod
    def construct_post_url(cls, managed_integration_uuid):
        return 'managed_integrations/public/{}/heartbeat'.format(
            managed_integration_uuid
        )

    def create(self, managed_integration_uuid):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        client.create_resource(
            self.construct_post_url(managed_integration_uuid), data=data
        )
