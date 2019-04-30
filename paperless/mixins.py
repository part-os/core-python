import attr

from .api_mappers import BaseMapper
from .json_encoders import BaseJSONEncoder
from .client import PaperlessClient


class FromJSONMixin(object):
    """

    """
    # TODO: RENAME TO json_decoder
    _mapper = BaseMapper

    @classmethod
    def from_json(cls, resource):
        return cls(**cls._mapper.map(resource))

class ReadMixin(object):

    @classmethod
    def construct_get_url(cls):
        # this is a hack because of how awful our api endpoints currently are
        raise NotImplementedError

    @classmethod
    def construct_get_params(cls):
        return None

    @classmethod
    def get(cls, id):
        client = PaperlessClient.get_instance()
        return cls.from_json(client.get_resource(
            cls.construct_get_url(),
            id,
            params=cls.construct_get_params())
        )


class ListMixin(object):
    _list_mapper = BaseMapper
    _list_object_representation = None

    @classmethod
    def construct_list_url(cls):
        #this is a hack because of how awful our api endpoints currently are
        raise NotImplementedError

    @classmethod
    def parse_list_response(cls, results):
        """
        an overridable method if your data comes in a weird format...
        """
        return results

    @classmethod
    def list(cls, params=None):
        client = PaperlessClient.get_instance()
        resource_list = cls.parse_list_response(
            client.get_resource_list(cls.construct_list_url(), params=params))
        print("resource list")
        print(resource_list)
        if cls._list_object_representation:
            return [cls._list_object_representation.from_json(resource) for resource in resource_list]
        else:
            return [cls.from_json(resource) for resource in resource_list]


class ToDictMixin(object):
    def to_dict(self):
        return attr.asdict(self, recurse=True)


class ToJSONMixin(object):
    """

    """
    _json_encoder = BaseJSONEncoder

    def to_json(self):
        return self._json_encoder.encode(self)


class UpdateMixin(object):
    _primary_key = "id"

    @classmethod
    def construct_post_url(cls):
        # this is a hack because of how awful our api endpoints currently are
        raise NotImplementedError

    @classmethod
    #PATCH OR PUT?
    def construct_patch_url(cls):
        # this is a hack because of how awful our api endpoints currently are
        raise NotImplementedError

    def save_children(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, UpdateMixin):
                print("we have a value to update value =")
                print("value")
                value.save()
                # TODO: UPDATE VALUE AFTER SAVE?
                #maybe.... something like this
                #setattr(self, attr, value.save())

    def save(self):
        client = PaperlessClient.get_instance()
        primary_key = getattr(self, self._primary_key)
        self.save_children()
        data = self.to_json()
        if primary_key and int(primary_key) > 0:
            # update
            client.update_resource(self.construct_put_url(), data=data)
            print("perform update")
        else:
            #create
            client.create_resource(self.construct_post_url(), data=data)
            #TODO: UPDATE OUR ID
            #JUST ID RIGHT?
            print("perform create")
