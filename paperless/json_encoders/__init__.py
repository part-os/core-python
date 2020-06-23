class BaseJSONEncoder(object):
    @classmethod
    def encode(cls, resource, json_dumps=True):
        raise NotImplementedError
