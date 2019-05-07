import json
import requests

#from .api_mappers import OrderDetailsMapper, OrderMinimumMapper
from .exceptions import PaperlessAuthorizationException, PaperlessException, PaperlessNotFoundException
#from .listeners import OrderListener

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
    # TODO: Find a better way to do authentication
    base_url = "https://api.paperlessparts.com"
    group_slug = None
    password = None
    token = None
    username = None
    version = VERSION_0

    def __new__(cls, **kwargs):
        """
        Create or return the PaperlessClient Singleton.
        """
        if PaperlessClient.__instance is None:
            PaperlessClient.__instance = object.__new__(cls)
        instance = PaperlessClient.__instance

        if 'base_url' in kwargs:
            instance.base_url = kwargs['base_url']

        if 'username' in kwargs:
            instance.username = kwargs['username']

        if 'password' in kwargs:
            instance.password = kwargs['password']

        if 'group_slug' in kwargs:
            instance.group_slug = kwargs['group_slug']

        if 'version' in kwargs: # TODO: ADD VERSION VALIDATION
            instance.version = kwargs['version']

        return instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def get_authenticated_headers(self):
        if not self.token:
            self.authenticate()

        return {
            'Accept': 'application/json',
            'Authorization': 'Token {}'.format(self.token),
            'Content-Type': 'application/json',
            'User-Agent': 'python-paperlessSDK V0 library'
        }

    def authenticate(self):
        """uses a suppliers login information to retrieve a valid bearer token"""
        # validate we have the proper values to authenticate
        required_fields = ['password', 'username']
        missing_fields = [field for field in required_fields if getattr(self, field) is None]
        if missing_fields:
            error_detail = ""
            for missing_field in missing_fields:
                error_detail += "Missing required field: " + missing_field
            raise PaperlessAuthorizationException(
                message="Unable to authenticate client.",
                detail=error_detail
            )

        data = {
            'password': self.password,
            'username': self.username
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-paperlessSDK V0 library'
        }

        resp = requests.post(
            "{}/{}".format(self.base_url, 'login'),
            data=json.dumps(data),
            headers=headers
        )

        if resp.status_code == 200:
            self.token = resp.json()['token']
        elif 200 < resp.status_code < 500:
            raise PaperlessAuthorizationException(
                detail=resp.json()['extra'],
                error_code=resp.status_code,
                message = resp.json()['message']
            )

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
        print(requests)
        resp = requests.get(
            req_url,
            headers=headers,
            params=params
        )

        if resp.status_code == 200:
            #return self.mappers[self.version][resource_type][self.GET].map(resource=resp.json())
            return resp.json()
        elif resp.status_code == 404: # Do I need to do this if this is the default?
            raise PaperlessNotFoundException(
                message="Unable to locate object with id {} from url: {}".format(id, req_url)
            )
        elif resp.status_code == 401 and resp.json()['code'] == 'authentication_failed':
            self.token = None
            return None

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