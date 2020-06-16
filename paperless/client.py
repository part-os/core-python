import json
import requests

from .exceptions import PaperlessAuthorizationException, PaperlessException, PaperlessNotFoundException


class PaperlessClient(object):
    GET = 'get'
    LIST = 'list'
    LOGIN = 'login'
    ORDERS = 'orders'
    PAYMENT_TERMS = 'payment_terms'
    QUOTES = 'quotes'

    VERSION_0 = 'v0.0'
    VALID_VERSIONS = [VERSION_0]

    __instance = None
    access_token = None
    base_url = "https://api.paperlessparts.com"
    group_slug = None
    version = VERSION_0

    def __new__(cls, **kwargs):
        """
        Create or return the PaperlessClient Singleton.
        """
        if PaperlessClient.__instance is None:
            PaperlessClient.__instance = object.__new__(cls)
        instance = PaperlessClient.__instance

        if 'access_token' in kwargs:
            instance.access_token = kwargs['access_token']

        if 'base_url' in kwargs:
            instance.base_url = kwargs['base_url']

        if 'group_slug' in kwargs:
            instance.group_slug = kwargs['group_slug']

        if 'version' in kwargs: # TODO: ADD VERSION VALIDATION
            instance.version = kwargs['version']

        return instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def get_authenticated_headers(self):
        if not self.access_token:
            raise PaperlessAuthorizationException(
                message='Unable to authenticate call',
                detail='You are trying to perform an HTTP request without a proper access token.'
            )

        return {
            'Accept': 'application/json',
            'Authorization': 'API-Token {}'.format(self.access_token),
            'Content-Type': 'application/json',
            'User-Agent': 'python-paperlessSDK {}'.format(self.version)
        }

    def get_resource_list(self, list_url, params=None):
        headers = self.get_authenticated_headers()
        resp = requests.get(
            "{}/{}".format(
                self.base_url,
                list_url
            ), # check for next number, assumes they are sequential
            headers=headers,
            params=params
        )
        return resp.json()

    def get_resource(self, resource_url, id, params=None):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        headers = self.get_authenticated_headers()

        req_url = "{}/{}/{}".format(self.base_url, resource_url, id)
        resp = requests.get(
            req_url,
            headers=headers,
            params=params
        )

        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            raise PaperlessNotFoundException(
                message="Unable to locate object with id {} from url: {}".format(id, req_url)
            )
        elif resp.status_code == 401 and resp.json()['code'] == 'authentication_failed':
            raise PaperlessAuthorizationException(
                message="Not authorized to access url: {}".format(req_url)
            )
        else:
            raise PaperlessException(
                message="Failed to get resource with id {} from url: {}".format(id, req_url),
                error_code=resp.status_code
            )

    def get_new_resources(self, resource_url, params=None):

        headers = self.get_authenticated_headers()

        req_url = "{}/{}".format(self.base_url, resource_url)
        resp = requests.get(
            req_url,
            headers=headers,
            params=params
        )

        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            raise PaperlessNotFoundException(
                message="Unable to get new resources from url: {}".format(req_url)
            )
        elif resp.status_code == 401 and resp.json()['code'] == 'authentication_failed':
            raise PaperlessAuthorizationException(
                message="Not authorized to access url: {}".format(req_url)
            )
        else:
            raise PaperlessException(
                message="Failed to get resources from url: {}".format(req_url),
                error_code=resp.status_code
            )

    def create_resource(self, resource_url, data):
        """
        """
        headers = self.get_authenticated_headers()

        req_url = '{}/{}'.format(self.base_url, resource_url)

        resp = requests.post(
            req_url,
            headers=headers,
            data=data
        )

        if resp.status_code == 201:
            return resp.json()
        else:
            raise PaperlessException(
                message="Failed to create resource",
                error_code=resp.status_code
            )

    def update_resource(self, resource_url, id, data):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        headers = self.get_authenticated_headers()

        req_url = '{}/{}/{}'.format(self.base_url, resource_url, id)

        resp = requests.patch(
            req_url,
            headers=headers,
            data=data
        )

        if resp.status_code == 200:
            return resp.json()
        else:
            raise PaperlessException(
                message="Failed to update resource",
                error_code=resp.status_code
            )

    def delete_resource(self, resource_url, id):
        """
        """
        headers = self.get_authenticated_headers()

        req_url = '{}/{}/{}'.format(self.base_url, resource_url, id)

        resp = requests.delete(
            req_url,
            headers=headers
        )
        if resp.status_code == 204:
            return
        else:
            raise PaperlessException(
                message="Failed to delete resource",
                error_code=resp.status_code
            )

    def download_file(self, resource_url, id, file_path, params=None):
        """
            download the file resource specified by resource_url and id
        """
        headers = self.get_authenticated_headers()

        req_url = "{}/{}/{}".format(self.base_url, resource_url, id)
        resp = requests.get(
            req_url,
            headers=headers,
            params=params
        )

        if resp.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
        elif resp.status_code == 404:
            raise PaperlessNotFoundException(
                message="Unable to locate object with id {} from url: {}".format(id, req_url)
            )
        elif resp.status_code == 401 and resp.json()['code'] == 'authentication_failed':
            raise PaperlessAuthorizationException(
                message="Not authorized to access url: {}".format(req_url)
            )
        else:
            raise PaperlessException(
                message="Failed to get resource with id {} from url: {}".format(id, req_url),
                error_code=resp.status_code
            )
