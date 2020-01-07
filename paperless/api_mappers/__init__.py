class BaseMapper(object):
    @classmethod
    def map(cls, resource):
        raise NotImplementedError
