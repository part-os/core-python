import csv
import json

from paperless.client import PaperlessClient


class CustomTable:
    config = None
    data = None

    def __init__(self, config=None, data=None):
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

    def update(self, table_name):
        """
        Persists local changes of an existing Paperless Parts resource to Paperless.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json({'config': self.config, 'data': self.data})
        resp_json = client.update_resource(
            self.construct_patch_url(), table_name, data=data
        )
        return resp_json

    @classmethod
    def construct_post_url(cls):
        return 'suppliers/public/custom_tables'

    def create(self, table_name):
        """
        Persist new version of self to Paperless Parts and updates instance with any new data from the creation.
        """
        client = PaperlessClient.get_instance()
        data = self.to_json({'name': table_name})
        resp_json = client.create_resource(self.construct_post_url(), data=data)
        return resp_json

    @classmethod
    def construct_download_csv_url(cls):
        return 'suppliers/public/custom_tables/csv_download'

    @classmethod
    def download_csv(cls, table_name, config=False, file_path=None):
        """
        Download a CSV of the table data. If config == True, download the config data for the table instead.
        """
        params = {'config': True} if config else None
        if file_path is None:
            file_path = f'table_{table_name}_{"config" if config else "data"}.csv'
        client = PaperlessClient.get_instance()
        client.download_file(
            cls.construct_download_csv_url(), table_name, file_path, params=params
        )

    @classmethod
    def construct_list_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def get_list(cls):
        client = PaperlessClient.get_instance()

        return client.get_new_resources(cls.construct_list_url(), params=None)

    @classmethod
    def construct_get_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def get(cls, table_name):
        client = PaperlessClient.get_instance()

        return client.get_resource(cls.construct_get_url(), table_name)

    @classmethod
    def construct_delete_url(cls):
        return 'suppliers/public/custom_tables'

    @classmethod
    def delete(cls, table_name):
        client = PaperlessClient.get_instance()

        return client.delete_resource(cls.construct_delete_url(), table_name)
