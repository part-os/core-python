import logging
from typing import Optional, Tuple

from .exceptions import PaperlessNotFoundException
from .local import LocalStorage
from .objects.orders import Order
from .objects.quotes import Quote

LOGGER = logging.getLogger(__name__)
LOCAL_STORAGE_PATH = 'processed_records.json'


class BaseListener:
    """
    An inheritable base listener for new object creation events
    """

    resource_type = None

    def __init__(
        self, filename=LOCAL_STORAGE_PATH, last_record_id: Optional[int] = None
    ):
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
        while resource is not None:
            try:
                success = self.on_event(resource)
            except Exception as e:
                success = False
                LOGGER.exception(
                    'Unhandled exception in listener, will not retry {}'.format(
                        self.get_resource_unique_identifier(resource)
                    )
                )
            self.record_resource_processed(resource, success)
            resource = self.get_new_resource()

    def get_resource_unique_identifier(self, resource):
        raise NotImplementedError

    def record_resource_processed(self, resource, success):
        """Records that an on_event for a resource was handled."""
        self.local_storage.process(
            self.resource_type, self.get_resource_unique_identifier(resource), success
        )

    def get_last_resource_processed(self) -> int:
        """Retrieves the resource ID from the latest successfully processed
        resource in the data store"""
        last_processed = self.local_storage.get_last_processed(self.resource_type)
        if last_processed is None:
            return self.get_default_last_record_id()
        else:
            return last_processed


class OrderListener(BaseListener):
    resource_type = Order

    def __init__(
        self, filename=LOCAL_STORAGE_PATH, last_record_id: Optional[int] = None
    ):
        super().__init__(filename, last_record_id)
        self._most_recent_order = last_record_id

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
                    order_list[0]
                )
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


class QuoteListener(BaseListener):
    resource_type = Quote

    def __init__(
        self,
        filename=LOCAL_STORAGE_PATH,
        last_record_id: Optional[int] = None,
        last_record_revision: Optional[int] = None,
    ):
        super().__init__(filename, last_record_id)
        self._most_recent_quote: Tuple[Optional[int], Optional[int]] = (
            last_record_id,
            last_record_revision,
        )

    def get_default_last_record_id(self):
        """
        Loads the quote list by ascending sent_date order and returns the newest quote's number and revision.

        :return: the order number of the newest order, or 0 if it is None
        """
        most_recent_quote_number, most_recent_quote_revision = self._most_recent_quote

        if (
            most_recent_quote_number is not None
        ):  # If the supplied quote number is not None, use the (quote_number, revision) pair regardless of whether revision is None
            return self._most_recent_quote
        else:
            quotes_list = Quote.get_new()
            try:
                most_recent_quote_result = quotes_list[-1]
                self._most_recent_quote = (
                    most_recent_quote_result['quote'],
                    most_recent_quote_result['revision'],
                )
            except IndexError:
                # Default to 0 with revision None if there are no quotes.
                # This will not work for suppliers with no quotes and
                # a configured starting quote number that is greater than 1.
                # In that case, you MUST specify a default_last_record_id.
                self._most_recent_quote = (0, None)
            return self._most_recent_quote

    def get_resource_unique_identifier(self, resource):
        return {'id': resource.number, 'revision': resource.revision_number}

    def get_new_resource(self):
        try:
            last_resource_processed = self.get_last_resource_processed()
            resource_id = last_resource_processed['id']
            resource_revision = last_resource_processed['revision']
            new_quotes = Quote.get_new(id=resource_id, revision=resource_revision)
            if new_quotes:
                first_new_quote_number = new_quotes[0]['quote']
                first_new_quote_revision = new_quotes[0]['revision']
                return Quote.get(first_new_quote_number, first_new_quote_revision)
            else:
                return None
        except PaperlessNotFoundException:
            return None

    def on_event(self, resource: Order):
        """
        Called to handle when a new Quote is processed.

        :param resource: Quote
        """
        raise NotImplementedError
