import csv
import json

from paperless.manager import BaseManager


class CustomTable:
    config = None
    data = None

    def __init__(self, client, config=None, data=None):
        self.client = client
        if config is not None:
            self.config = self.validate_config_data(config)
        if data is not None:
            self.data = self.validate_table_data(data)

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
                raise ValueError("The supplied data must be an array of objects")
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

    def to_json(self, data):
        return json.dumps(data)

    @classmethod
    def construct_patch_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def construct_post_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def construct_download_csv_url(cls):
        return 'suppliers/public/custom_tables/csv_download'

    @classmethod
    def construct_list_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def construct_delete_url(cls):
        return 'suppliers/public/custom_tables'


class CustomTableManager(BaseManager):
    _base_object = CustomTable

    def delete(self, table_name):
        client = self._client

        return client.delete_resource(
            self._base_object.construct_delete_url(), table_name
        )

    def get(self, table_name):
        client = self._client

        return client.get_resource(self._base_object.construct_get_url(), table_name)

    def get_list(self):
        client = self._client

        return client.get_new_resources(
            self._base_object.construct_list_url(), params=None
        )

    def download_csv(self, table_name, config=False, file_path=None):
        """
        Download a CSV of the table data. If config == True, download the config data for the table instead.
        """
        params = {'config': True} if config else None
        if file_path is None:
            file_path = f'table_{table_name}_{"config" if config else "data"}.csv'
        client = self._client
        client.download_file(
            self._base_object.construct_download_csv_url(),
            table_name,
            file_path,
            params=params,
        )

    def create(self, obj, table_name):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = self._client
        data = obj.to_json({'name': table_name})
        resp_json = client.create_resource(
            self._base_object.construct_post_url(), data=data
        )
        return resp_json

    def update(self, obj, table_name):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        data = self.to_json({'config': obj.config, 'data': obj.data})
        resp_json = self._client.update_resource(
            self.construct_patch_url(), table_name, data=data
        )
        return resp_json
