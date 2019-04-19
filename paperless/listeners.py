from .api_mappers import OrderMapper

# thought: add a listen mixin so this class has a listen, but also defines the common method that must be implemented,
class BaseListener:
    client = None
    last_updated = None
    response_mapper = None
    type = None

    def __init__(self, last_updated: int): #don't really like this name...
        self.last_updated = last_updated

    def get_new_resource(self): #get new? get next? get latest?
        """SHOULD CALL A FUNCTION THAT CHECKS FOR UPDATES BASED ON ITS INTERNAL PATTERNS"""
        return self.client.check_for_next_resource(self.type, self.last_updated)

    def on_event(self, resource):
        raise NotImplementedError

    def listen(self):
        new_resource_exists, resource = self.get_new_resource()
        if new_resource_exists:
            self.on_event(resource)
            # if on event was processed
            self.last_updated = self.get_resource_unique_identifier(resource)

    # NOT SURE IF I LOVE THIS BEING A CLASS METHOD AND NOT BELONGING TO THE RESOURCE?
    @staticmethod
    def get_resource_unique_identifier(self, resource):
        raise NotImplementedError


class OrderListener(BaseListener):
    type = "order"

    def get_resource_unique_identifier(self, resource):
        return resource.number
