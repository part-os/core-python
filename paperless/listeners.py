from typing import Optional

from .local import LocalStorage
from .exceptions import PaperlessNotFoundException
from .objects.orders import Order


LOCAL_STORAGE_PATH = 'processed_records.json'


class BaseListener:
    """
    An inheritable base listener for new object creation events
    """
    resource_type = None

    def __init__(self, filename=LOCAL_STORAGE_PATH,
                 last_record_id: Optional[int] = None):
        """
        Sets up the initial state of the listener by either loading it from
        local storage or initializing with reasonable defaults.

        :param: filename for local storage
        :param last_record_id: resource identifier, all future resources will be
        indexed AFTER this one
        """
        self.local_storage = LocalStorage.get_instance(filename)
        self.default_last_record_id = last_record_id

    def get_default_last_record_id(self) -> int:
        """ Returns the unique resource identifier which will determine where
        we begin to look for future resources."""
        raise NotImplementedError

    def get_new_resource(self):
        raise NotImplementedError

    def on_event(self, resource):
        raise NotImplementedError

    def listen(self):
        resource = self.get_new_resource()
        #while resource is not None:
        if resource is not None:
            success = self.on_event(resource)
            self.record_resource_processed(resource, success)
            #resource = self.get_new_resource()

    @staticmethod
    def get_resource_unique_identifier(self, resource):
        raise NotImplementedError

    def record_resource_processed(self, resource, success):
        """Records that an on_event for a resource was handled."""
        self.local_storage.process(
            self.resource_type,
            self.get_resource_unique_identifier(resource),
            success
        )

    def get_last_resource_processed(self) -> int:
        """Retrieves the resource ID from the latest successfully processed
        resource in the data store"""
        last_processed = self.local_storage.get_last_processed(
            self.resource_type)
        if last_processed is None:
            return self.get_default_last_record_id()
        else:
            return last_processed


class OrderListener(BaseListener):
    resource_type = Order

    def __init__(self, filename=LOCAL_STORAGE_PATH,
                 last_record_id: Optional[int] = None):
        super().__init__(filename, last_record_id)
        self._most_recent_order = None

    def get_default_last_record_id(self):
        """
        Loads the order list by descending order number order and returns the newest orders number.

        :return: the order number of the newest order, or 0 if it is None
        """
        if self._most_recent_order is not None:
            return self._most_recent_order
        else:
            order_list = Order.list(params={'o': '-number'})
            try:
                self._most_recent_order = self.get_resource_unique_identifier(
                    order_list[0])
            except IndexError:
                # Default to 0 if there are no orders.
                # This will not work for suppliers with no orders and
                # a configured starting order number that is greater than 1.
                # In that case, you MUST specify a default_last_record_id.
                self._most_recent_order = 0
            return self._most_recent_order

    def get_resource_unique_identifier(self, resource):
        return resource.number

    def get_new_resource(self):
        try:
            return Order.get(self.get_last_resource_processed() + 1)
        except PaperlessNotFoundException:
            return None

    def on_event(self, resource: Order):
        """
        Called to handle when a new Order is processed.

        :param resource: Order
        """
        raise NotImplementedError
