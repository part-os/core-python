import json
import requests

from .listeners import OrderListener
from .api_mappers import OrderMapper

class PaperlessClient(object):
    __instance = None
    # TODO: Find a better way to do authentication
    group = None
    password = None
    token = None
    username = None
    version = None

    LOGIN = 'login'
    ORDERS = OrderListener.type
    QUOTES = 'quotes'

    VERSION_0 = 'v0.0'
    VALID_VERSIONS = [VERSION_0]

    urls = {
        VERSION_0: {
            LOGIN: "https://dev.paperlessparts.com/api/login",
            ORDERS: "https://dev.paperlessparts.com/api/orders/by_number/",
            QUOTES: "https://dev.paperlessparts.com/api/quotes/by_number/"
        }
    }

    mappers = {
        VERSION_0: {
            ORDERS: OrderMapper,
        }
    }

    def __new__(cls, **kwargs):
        if PaperlessClient.__instance is None:
            PaperlessClient.__instance = object.__new__(cls)
        instance = PaperlessClient.__instance

        # TODO: I THINK THESE KWARGS SHOULD BE EXPLICITLY DEFINED
        if 'username' in kwargs:
            instance.username = kwargs['username']

        if 'password' in kwargs:
            instance.password = kwargs['password']

        if 'group_slug' in kwargs:
            instance.group_slug = kwargs['group_slug']

        if 'version' in kwargs: # TODO: ADD VERSION VALIDATION
            instance.version = kwargs['version']

        #TODO: ASSERT VERSION IS AVAILABLE AND VALID
        return instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

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
        #TODO: RAISE NOT AUTHENTICAED ERROR or AUTHENTICATION FAILED ERROR
        return

    def check_for_next_resource(self, resource_type, last_updated):
        """
            takes a resource type, uses that type to find the url,
            then it will perform call for last updated + 1
            and respond false if that is a 404
        """
        if not self.token:
            self.authenticate()

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Token {}'.format(self.token),
            'Content-Type': 'application/json',
            'User-Agent': 'python-paperlessSDK V0 library'
        }

        resp = requests.get(
            "{}/{}".format(self.urls[self.version][resource_type], last_updated + 1), # check for next number, assumes they are sequential
            headers=headers,
            params={'group': self.group_slug}
        )

        if resp.status_code is 200:
            #todo: map to object
            return True, self.mappers[self.version][resource_type].map(resource=resp.json())
        elif resp.status_code is 404: # Do I need to do this if this is the default?
            return False, None
        elif resp.status_code is 401 and resp.json()['code'] is 'authentication_failed':
            # TODO: DO I also need to verify this was 'authentication failed' and not for permission denied?
            self.token = None

        return False, None

