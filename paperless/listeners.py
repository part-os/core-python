import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .exceptions import PaperlessNotFoundException
from .objects.orders import Order

class BaseListener:
    """
    An inheritable base listener for new object creation events
    """
    data_store = None
    last_updated = None
    type = None

    def __init__(self, last_updated: Optional[int] = None):
        """
        Sets up the initial state of the listener by either:
        1. defaulting to the existing datastore located in the data_store file
        2. initializing the datastore, if it does not currently exist, with the
        initial value passed through last_updated.
        2. uses the custom implementation in the get_first_resource_identifier
        method to determine where initialization should begin.

        :param last_updated: resource identifier, all future resources will be indexed AFTER this one
        """
        datafile = Path(self.data_store)
        if not datafile.is_file():
            # create file for persisting state
            with open(self.data_store, "w+") as json_file:
                if last_updated is None:
                    last_updated = self.get_first_resource_identifier()
                json.dump([{'processed_on': str(datetime.now()), 'resource': last_updated}], json_file)

    def get_first_resource_identifier(self) -> int:
        """ Returns the unique resource identifier which will determine where we begin to look for future resources."""
        raise NotImplementedError

    def get_new_resource(self):
        raise NotImplementedError

    def on_event(self, resource):
        raise NotImplementedError

    def listen(self):
        resource = self.get_new_resource()
        if resource is not None:
            self.on_event(resource)
            # on_event was processed successfully
            self.record_successful_resource_process(resource)

    @staticmethod
    def get_resource_unique_identifier(self, resource):
        raise NotImplementedError

    def record_successful_resource_process(self, resource):
        """ Records that an on_event for a resource was handled successfully. """
        with open(self.data_store, "r") as json_file:
            data = json.load(json_file)
        data.append({'processed_on': str(datetime.now()), 'resource': self.get_resource_unique_identifier(resource)})
        with open(self.data_store, "w") as json_file:
            json.dump(data, json_file)

    def get_last_resource_processed(self) -> int:
        """
            Retrieves the resource ID from the latest
            successfully processed resource in the data store
        """
        with open(self.data_store, "r") as json_file:
            data = json.load(json_file)
        try:
            return data[-1]['resource']
        except (IndexError, KeyError):
            return None

class OrderListener(BaseListener):
    data_store = ".processed_orders.json"

    def get_first_resource_identifier(self):
        """
        Loads the order list by descending order number order and returns the newest orders number.

        :return: the order number of the newest order, or 0 if it is None
        """
        order_list = Order.list(params={'o': '-created'})
        try:
            return self.get_resource_unique_identifier(order_list[0])
        except IndexError:
            """
            Default to 0 if there are no orders.
            
            This may cause an issue for suppliers with no orders and 
            a configured starting order number that is greater than 1.
            """
            return 0

    def get_resource_unique_identifier(self, resource):
        """ returns order.number """
        # TODO: BRING TO THE OBJECT LEVEL
        return resource.number

    def get_new_resource(self):
        try:
            return Order.get(self.get_last_resource_processed() + 1)
        except PaperlessNotFoundException:
            return None
