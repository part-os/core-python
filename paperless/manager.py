from paperless.client import PaperlessClient
import urllib.parse as urlparse
from urllib.parse import parse_qs
import types


class BaseManager:

    _client = None
    _base_object = None

    def __init__(self, client: PaperlessClient) -> None:
        self._client = client

    def get(self, id):
        """
        Retrieves the resource specified by the id.
        :raise PaperlessNotFoundException: Raised when the requested id 404s aka is not found.
        :param id: int
        :return: resource
        """
        client = self._client
        return self._base_object.from_json(
            client.get_resource(
                self._base_object.construct_get_url(), id, params=self._base_object.construct_get_params()
            )
        )

    def get_new(self, id=None):
        client = self._client

        return client.get_new_resources(
            self._base_object.construct_get_new_resources_url(),
            params=self.construct_get_new_params(id) if id else None,
        )

    def list(self, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = self._client
        if getattr(self._base_object, "construct_paginated_list_url", None):
            return self.paginated_list(params=params)
        resource_list = self._base_object.parse_list_response(
            client.get_resource_list(self._base_object.construct_list_url(), params=params)
        )
        if self._base_object._list_object_representation:
            return [
                self._base_object._list_object_representation.from_json(resource)
                for resource in resource_list
            ]
        else:
            return [self._base_object.from_json(resource) for resource in resource_list]

    def paginated_list(self, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :param pages: iterable of ints describing the indices of the pages you want (starting from 1)
        :return: [resource]
        """
        client = client = self._client
        response = client.get_resource_list(self._base_object.construct_paginated_list_url(), params=params)
        resource_list = self._base_object.parse_list_response(response)
        while response['next'] is not None:
            next_url = response['next']
            next_query_params = parse_qs(urlparse.urlparse(next_url).query)
            if params is not None:
                next_query_params = {**next_query_params, **params}
            response = client.get_resource_list(
                self._base_object.construct_paginated_list_url(), params=next_query_params
            )
            resource_list.extend(self._base_object.parse_list_response(response))
        return [self._base_object.from_json(resource) for resource in resource_list]

    def create(self, obj):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = self._client
        data = obj.to_json()
        resp = client.create_resource(self._base_object.construct_post_url(), data=data)
        resp_obj = self._base_object.from_json(resp)
        keys = filter(
            lambda x: not x.startswith('__')
            and not x.startswith('_')
            and type(getattr(resp_obj, x)) != types.MethodType,
            dir(resp_obj),
        )
        for key in keys:
            setattr(obj, key, getattr(resp_obj, key))
    
    def delete(self, obj):
        """
        Deletes the resource from Paperless Parts.
        """
        client = self._client
        primary_key = getattr(self, obj._primary_key)
        client.delete_resource(self._base_object.construct_delete_url(), primary_key)

    def update(self, obj):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        client = self._client
        primary_key = getattr(self, obj._primary_key)
        data = obj.to_json()
        resp = client.update_resource(
            self._base_object.construct_patch_url(), primary_key, data=data
        )
        resp_obj = self._base_object.from_json(resp)
        # This filter is designed to remove methods, properties, and private data members and only let through the
        # fields explicitly defined in the class definition
        keys = filter(
            lambda x: not x.startswith('__')
            and not x.startswith('_')
            and type(getattr(resp_obj, x)) != types.MethodType
            and (
                not isinstance(getattr(resp_obj.__class__, x), property)
                if x in dir(resp_obj.__class__)
                else True
            ),
            dir(resp_obj),
        )
        for key in keys:
            setattr(self, key, getattr(resp_obj, key))
