import json
import requests

from .api_mappers import OrderDetailsMapper, OrderMinimumMapper
from .exceptions import PaperlessAuthorizationException
from .listeners import OrderListener

class PaperlessClient(object):
    GET = 'get'
    LIST = 'list'
    LOGIN = 'login'
    ORDERS = OrderListener.type
    QUOTES = 'quotes'

    VERSION_0 = 'v0.0'
    VALID_VERSIONS = [VERSION_0]

    __instance = None
    # TODO: Find a better way to do authentication
    group_slug = None
    password = None
    token = None
    username = None
    version = VERSION_0

    urls = {
        VERSION_0: {
            LOGIN: "https://dev.paperlessparts.com/api/login",
            ORDERS: {
                GET: "https://dev.paperlessparts.com/api/orders/by_number/",
                LIST: "https://dev.paperlessparts.com/api/orders/groups/"
            },
            QUOTES: {
                GET: "https://dev.paperlessparts.com/api/quotes/by_number/"
            }
        }
    }

    """urls = {
        VERSION_0: {
            LOGIN: "https://api.paperlessparts.com/login",
            ORDERS: {
                GET: "https://api.paperlessparts.com/orders/by_number/",
                LIST: "https://api.paperlessparts.com/orders/groups/"
            },
            QUOTES: {
                GET: "https://dev.paperlessparts.com/api/quotes/by_number/"
            }
        }
    }"""

    mappers = {
        VERSION_0: {
            ORDERS: {
                GET: OrderDetailsMapper,
                LIST: OrderMinimumMapper
            },
        }
    }

    def __new__(cls, **kwargs):
        """
        Create or return the PaperlessClient Singleton.
        """
        if PaperlessClient.__instance is None:
            PaperlessClient.__instance = object.__new__(cls)
        instance = PaperlessClient.__instance

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
        # TODO: ASSERT WE HAVE AN EMAIL AND A PASSWORD
        data = {
            'password': self.password,
            'username': self.username
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'python-paperlessSDK V0 library'
        }


        resp = requests.post(self.urls[self.version][self.LOGIN], data=json.dumps(data), headers=headers)

        if resp.status_code is 200:
            self.token = resp.json()['token']
        elif 200 < resp.status_code < 500:
            raise PaperlessAuthorizationException(
                detail=resp.json()['extra'],
                error_code=resp.status_code,
                message = resp.json()['message']
            )

    def check_for_next_resource(self, resource_type, last_updated) -> (bool, object):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        headers = self.get_authenticated_headers()

        resp = requests.get(
            "{}/{}".format(self.urls[self.version][resource_type][self.GET], last_updated + 1), # check for next number, assumes they are sequential
            headers=headers,
            params={'group': self.group_slug}
        )

        if resp.status_code is 200:
            #todo: map to object
            return True, self.mappers[self.version][resource_type][self.GET].map(resource=resp.json())
        elif resp.status_code is 404: # Do I need to do this if this is the default?
            return False, None
        elif resp.status_code is 401 and resp.json()['code'] is 'authentication_failed':
            self.token = None
        return False, None

    def get_resource_list(self, resource_type, params={}):
        headers = self.get_authenticated_headers()
        resp = requests.get(
            "{}/{}".format(self.urls[self.version][resource_type][self.LIST], self.group_slug), # check for next number, assumes they are sequential
            headers=headers,
            params=params
        )

        return self.mappers[self.version][resource_type][self.LIST].map(resource=resp.json()['results'])
