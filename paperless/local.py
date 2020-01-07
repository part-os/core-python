"""Local storage for keeping track of which entities have been processed.

There is a lightweight base class and a trivial JSON file implementation. Using
SQLite would be an obvious enhancement to provide better data integrity and
performance for large numbers of records.
"""
import os
import json
import datetime
import time


class LocalStorage:
    """Abstract base class for a local storage that tracks which records have
    been processed. ``resource_type`` is a class from the ``objects``
    package."""
    def __init__(self, filename):
        self.filename = filename

    def get_last_processed(self, resource_type):
        """Get the ID of the last processed resource of type
        ``resource_type``"""
        raise NotImplemented

    def clear_cache(self, resource_type=None):
        """Clear local storage for resources of type ``resource_type``. If
        ``resource_type`` is None, then the entire local storage will be
        cleared."""
        raise NotImplemented

    def process(self, resource_type, resource_id, success, dt=None):
        """
        Record that a resource has been processed.

        :param resource_type: the resource type
        :param resource_id: the primary key ID of the resource
        :param success: True or False
        :param dt: optional datetime; defaults to current time
        """
        raise NotImplemented

    @staticmethod
    def get_instance(filename):
        """Factory method for default LocalStorage implementation"""
        return DEFAULT_IMPLEMENTATION(filename)


class LocalJSONStorage(LocalStorage):
    def __init__(self, filename):
        super().__init__(filename)
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.store = json.load(f)
        else:
            self.store = {}
            self._write()

    def _write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f)
        # This is a hack to make sure we don't process the same record twice. We were seeing isues
        # due to non-atomic file writes
        time.sleep(0.5)

    def get_last_processed(self, resource_type):
        assert(isinstance(resource_type, type))
        key = resource_type.__name__
        if key in self.store and len(self.store[key]) > 0:
            # Return the ID of the most recently processed record. Quotes are not necessarily processed in increasing
            # order of ID so it's important to do the comparison based on timestamp
            return max(self.store[key], key=lambda x: x['dt'])['id']
        else:
            return None

    def clear_cache(self, resource_type=None):
        if resource_type is None:
            self.store = {}
        else:
            assert(isinstance(resource_type, type))
            key = resource_type.__name__
            self.store[key] = []
        self._write()

    def process(self, resource_type, resource_id, success, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        key = resource_type.__name__
        if key not in self.store:
            self.store[key] = []
        self.store[key].append({
            'id': resource_id,
            'dt': dt_str,
            's': success
        })
        self._write()


DEFAULT_IMPLEMENTATION = LocalJSONStorage
