import attr

from .api_mappers import BaseMapper
from .json_encoders import BaseJSONEncoder
from .client import PaperlessClient


class FromJSONMixin(object):
    """
    Takes a JSON response with the specific format from the Paperless API and returns a new instance of this resource.

    Note: The response from the API will not necessarily neatly map to this resource.
    Because of this, use the _mapper to specify how to map from the API to your resource.

    As an implementation note, we typically DO want to create a mapper function, even if the API response is 1 to 1
    with our class. The reason for this, is because the mapper acts as a filter that prevents additional fields from
    being passed to the attrs classes which would cause attrs to fail. This gives the flexibility to add new fields to
    the endpoint without having to worry about versioning...yet.
    """
    @classmethod
    def from_json_to_dict(cls, resource):
        # print(resource)
        # optionally map the resource to the correct structure
        if hasattr(cls, '_mapper'):
            return cls._mapper.map(resource)
        else:
            return resource

    @classmethod
    def from_json(cls, resource):
        return cls(**cls.from_json_to_dict(resource))

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
    def construct_get_new_params(cls,id):

        return {'last_quote': id}

    @classmethod
    def get(cls, id):
        """
        Retrieves the resource specified by the id.


        :raise PaperlessNotFoundException: Raised when the requested id 404s aka is not found.
        :param id: int
        :return: resource
        """
        client = PaperlessClient.get_instance()
        # print(id)
        return cls.from_json(client.get_resource(
            cls.construct_get_url(),
            id,
            params=cls.construct_get_params())
        )

    @classmethod
    def get_new(cls, id):
        client = PaperlessClient.get_instance()

        return client.get_new_resources(
            cls.construct_get_new_resources_url(),
            params=cls.construct_get_new_params(id)
        )


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

    @classmethod
    def list(cls, params=None):
        """
        Returns a list of (1) either the minimal representation of this resource as defined by _list_object_representation or (2) a list of this resource.

        :param params: dict of params for your list request
        :return: [resource]
        """
        client = PaperlessClient.get_instance()
        resource_list = cls.parse_list_response(
            client.get_resource_list(cls.construct_list_url(), params=params))
        if cls._list_object_representation:
            return [cls._list_object_representation.from_json(resource) for resource in resource_list]
        else:
            return [cls.from_json(resource) for resource in resource_list]


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


class CreateMixin(object):
    @classmethod
    def construct_post_url(cls):
        """
        Constructs a url to be used for placing post requests too.

        :return: string url
        """
        raise NotImplementedError

    def create(self):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.create_resource(self.construct_post_url(), data=data)
        resp_dict = self.from_json_to_dict(resp)
        for key, val in resp_dict.items():
            setattr(self, key, val)


class UpdateMixin(object):
    _primary_key = 'id'

    def construct_patch_url(cls):
        """
        Constructs a url to be used for placing past requests too.

        :return: string url
        """
        raise NotImplementedError

    def update(self):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        client = PaperlessClient.get_instance()
        primary_key = getattr(self, self._primary_key)
        data = self.to_json()
        resp = client.update_resource(self.construct_patch_url(), primary_key, data=data)
        resp_dict = self.from_json_to_dict(resp)
        for key, val in resp_dict.items():
            setattr(self, key, val)