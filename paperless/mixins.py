import json
import types

import attr

from .api_mappers import BaseMapper
from .json_encoders import BaseJSONEncoder


class FromJSONMixin(object):
    """
    Takes a JSON response with the specific format from the Paperless API and returns a new instance of this resource.

    Note: The response from the API will not necessarily neatly map to this resource.
    Because of this, use the _mapper to specify how to map from the API to your resource.
    """

    @classmethod
    def from_json_to_dict(cls, resource):
        if hasattr(cls, '_mapper'):
            return cls._mapper.map(resource)
        else:
            return resource

    @classmethod
    def from_json(cls, resource: dict):
        try:
            d = dict()
            cls_attrs = [a.name for a in attr.fields(cls)]
            for k, v in resource.items():
                if k in cls_attrs:
                    d[k] = v
        except attr.exceptions.NotAnAttrsClassError:
            d = resource
        return cls(**cls.from_json_to_dict(d))

    def update_with_response_data(self, response_data):
        """
        Update this instance with data from the given API response dictionary.
        """
        resp_obj = self.from_json(response_data)
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


class ReadMixin(object):
    @classmethod
    def construct_get_url(cls):
        """
        Constructs url for a GET request to retrieve specific version of this resource.

        :return: String url
        """
        raise NotImplementedError

    @classmethod
    def construct_get_params(cls):
        """
        Optional method to define query params to send along GET request

        :return None or params dict
        """
        return None

    @classmethod
    def construct_get_new_params(cls, id):
        return None


class ListMixin(object):
    _list_mapper = BaseMapper
    _list_object_representation = None

    @classmethod
    def construct_list_url(cls):
        """
        Constructs the url to get a list of resources from.

        :return: String url
        """
        raise NotImplementedError

    @classmethod
    def parse_list_response(cls, results):
        """
        An optional overridable method in case your list resources come back in a format other than a json list representation of itself.

        For instance, maybe your list endpoint returns an object including pagination instructions as well as the resource list. You would use this method to strip down to just the resource list.

        :return: json list of your resource
        """
        return results


class PaginatedListMixin(object):
    @classmethod
    def construct_paginated_list_url(cls):
        """
        Constructs the url to get a list of resources from.

        :return: String url
        """
        raise NotImplementedError

    @classmethod
    def parse_list_response(cls, results):
        """
        An optional overridable method in case your list resources come back in a format other than a json list representation of itself.

        For instance, maybe your list endpoint returns an object including pagination instructions as well as the resource list. You would use this method to strip down to just the resource list.

        :return: json list of your resource
        """
        return results['results']


class ToDictMixin(object):
    """
    Returns a dict representation of itself.

    :return: dict
    """

    def to_dict(self):
        return attr.asdict(self, recurse=True)


class ToJSONMixin(object):
    """
    Transforms self into a json object as expected to be serialized by the Paperless API.

    :returns: json
    """

    _json_encoder = BaseJSONEncoder

    def to_json(self):
        return self._json_encoder.encode(self)

    @classmethod
    def get_request_payload_from_instances(self, instances):
        """
        Transform list of instances into JSON request.
        """
        instance_dict_list = []
        for instance in instances:
            instance_dict = self._json_encoder.encode(instance, json_dumps=False)
            instance_dict_list.append(instance_dict)
        data_dict = {self._list_key: instance_dict_list}
        return json.dumps(data_dict)


class CreateMixin(object):
    @classmethod
    def construct_post_url(cls):
        raise NotImplementedError


class UpdateMixin(object):
    _primary_key = 'id'

    @classmethod
    def construct_patch_url(cls):
        raise NotImplementedError


class DeleteMixin(object):
    _primary_key = 'id'

    def construct_delete_url(cls):
        raise NotImplementedError


class BatchMixin(object):
    _list_key = (
        'override_this'
    )  # The field in the request schema in which to supply the list of objects

    @classmethod
    def construct_batch_url(cls, **kwargs):
        raise NotImplementedError
