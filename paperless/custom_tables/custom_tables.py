import csv

from paperless.client import PaperlessClient
from paperless.mixins import ToJSONMixin


class BaseCustomTable(ToJSONMixin):
    config = None
    data = None

    def __init__(self, config_data=None, table_data=None):
        if config_data is not None:
            self.config = self.validate_config_data(config_data)
        if table_data is not None:
            self.data = self.validate_table_data(table_data)

    def validate_config_data(self, config):
        if not isinstance(config, list):
            raise ValueError(
                "The supplied config must be an array of objects with keys 'column_name' and 'value_type'"
            )
        for col_config in config:
            if not isinstance(col_config, dict):
                raise ValueError(
                    "The supplied config must be an array of objects with keys 'column_name' and 'value_type'"
                )
            else:
                if set(col_config.keys()) != {'column_name', 'value_type'}:
                    raise ValueError(
                        "The supplied config must be an array of objects with keys 'column_name' and 'value_type'"
                    )
        return config

    def validate_table_data(self, data):
        if not isinstance(data, list):
            raise ValueError("The supplied data must be an array of objects")
        for col_data in data:
            if not isinstance(col_data, dict):
                raise ValueError(
                    "The supplied data must be an array of objects"
                )
        return data

    def from_csv(self, config_csv_file_path, data_csv_file_path=None):
        config_data = []
        table_data = []
        
        with open(config_csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                config_data.append(row)
        
        self.config = self.validate_config_data(config_data)

        if data_csv_file_path is not None:
            with open(data_csv_file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    table_data.append(row)

            self.data = self.validate_table_data(table_data)

    @classmethod
    def construct_patch_url(cls):
        return 'suppliers/public/custom_tables'

    def update(self, table_primary_key):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json()
        resp = client.update_resource(self.construct_patch_url(), table_primary_key, data=data)
        resp_dict = self.from_json_to_dict(resp)
        for key, val in resp_dict.items():
            setattr(self, key, val)

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/custom_tables'

    # TODO - define a from_json method
    # @classmethod
    # def get(cls, table_primary_key):
    #     """
    #     Retrieves the resource specified by the id.
    #
    #
    #     :raise PaperlessNotFoundException: Raised when the requested id 404s aka is not found.
    #     :param id: int
    #     :return: resource
    #     """
    #     client = PaperlessClient.get_instance()
    #     return cls.from_json(client.get_resource(
    #         cls.construct_get_url(),
    #         table_primary_key,
    #         params=cls.construct_get_params())
    #     )

    @classmethod
    def construct_list_url(cls):
        client = PaperlessClient.get_instance()
        return 'suppliers/public/{}/custom_tables'.format(client.group_slug)

    # TODO - define a function for getting the list of tables
    # @classmethod
    # def get_new(cls, id=None):
    #     client = PaperlessClient.get_instance()
    #
    #     return client.get_new_resources(
    #         cls.construct_get_new_resources_url(),
    #         params=cls.construct_get_new_params(id) if id else None
    #     )