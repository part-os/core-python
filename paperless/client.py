import json
import logging
import sys
import time
from types import SimpleNamespace

import requests

from .exceptions import (
    PaperlessAuthorizationException,
    PaperlessException,
    PaperlessNotFoundException,
)

LOGGER = logging.getLogger(__name__)


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

    METHODS = SimpleNamespace(
        DELETE='delete', GET='get', PATCH='patch', POST='post', PUT='put'
    )

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

        if 'version' in kwargs:  # TODO: ADD VERSION VALIDATION
            instance.version = kwargs['version']

        return instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def get_authenticated_headers(self):
        if not self.access_token:
            raise PaperlessAuthorizationException(
                message='Unable to authenticate call',
                detail='You are trying to perform an HTTP request without a proper access token.',
            )

        return {
            'Accept': 'application/json',
            'Authorization': 'API-Token {}'.format(self.access_token),
            'Content-Type': 'application/json',
            'User-Agent': 'python-paperlessSDK {}'.format(self.version),
        }

    def request(self, url=None, method=None, data=None, params=None, retries=None):
        req_url = f'{self.base_url}/{url}'

        headers = self.get_authenticated_headers()

        method_to_call = getattr(requests, method)
        if data is not None:
            resp = method_to_call(req_url, headers=headers, data=data, params=params)
        else:
            resp = method_to_call(req_url, headers=headers, params=params)

        if (
            resp.status_code == 200
            or resp.status_code == 201
            or resp.status_code == 204
        ):
            return resp
        elif resp.status_code == 429:
            try:
                message = resp.json().get('message')
                LOGGER.info(message)
                wait_time = (
                    int(message[message.find('in') + 3 : message.find('second') - 1])
                    + 1
                )
                time.sleep(wait_time)
            except (
                TypeError,
                AttributeError,
                ValueError,
            ) as e:  # catch any exception while trying to access the backoff message
                LOGGER.error(e)
                time.sleep(60)
            finally:
                return self.request(url=url, method=method, data=data, params=params)
        elif resp.status_code == 400:
            raise PaperlessException(
                message="Failed to update resource: {}".format(resp.content),
                error_code=resp.status_code,
            )
        elif resp.status_code == 401 and resp.json()['code'] == 'authentication_failed':
            raise PaperlessAuthorizationException(
                message="Not authorized to access url: {}".format(req_url)
            )
        elif resp.status_code == 404:
            raise PaperlessNotFoundException(
                message="Unable to locate object at url: {}".format(url)
            )
        elif resp.status_code == 502:
            if retries is None:
                retries = 0
            if retries < 5:
                LOGGER.info("Received 502. Waiting 30 seconds to retry.")
                time.sleep(30)
                return self.request(url=url, method=method, data=data, params=params, retries=retries + 1)
            else:
                raise PaperlessException(
                    message="Request failed", error_code=resp.status_code
                )
        else:
            try:
                resp_json = resp.json()
                message = resp_json['message']
            # raise generic error if there is no error message
            except Exception:
                raise PaperlessException(
                    message="Request failed", error_code=resp.status_code
                )
            raise PaperlessException(message=message, error_code=resp.status_code)

    def get_resource_list(self, list_url, params=None):
        resp = self.request(url=list_url, method=self.METHODS.GET, params=params)
        return resp.json()

    def get_resource(self, resource_url, id, params=None):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        url = "{}/{}".format(resource_url, id)
        print(url)
        resp = self.request(url=url, method=self.METHODS.GET, params=params)
        return resp.json()

    def get_new_resources(self, resource_url, params=None):

        # req_url = "{}/{}".format(self.base_url, resource_url)
        resp = self.request(url=resource_url, method=self.METHODS.GET, params=params)
        return resp.json()

    def create_resource(self, resource_url, data):
        """
        """
        resp = self.request(url=resource_url, method=self.METHODS.POST, data=data)
        return resp.json()

    def update_resource(self, resource_url, id, data, params=None):
        """
        """
        req_url = '{}/{}'.format(resource_url, id)
        if params is not None:
            resp = self.request(url=req_url, method=self.METHODS.PATCH, data=data, params=params)
        else:
            resp = self.request(url=req_url, method=self.METHODS.PATCH, data=data)

        return resp.json()

    def delete_resource(self, resource_url, id):
        """
        """
        headers = self.get_authenticated_headers()

        req_url = '{}/{}'.format(resource_url, id)

        resp = self.request(url=req_url, method=self.METHODS.DELETE)
        return

    def download_file(self, resource_url, id, file_path, params=None):
        """
            download the file resource specified by resource_url and id
        """

        req_url = "{}/{}".format(resource_url, id)
        resp = self.request(req_url, method=self.METHODS.GET, params=params)
        with open(file_path, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
