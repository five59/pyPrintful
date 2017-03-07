from decimal import Decimal
import json
import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth
from .pfException import pfException
from .pfAPIException import pfAPIException


class pyPrintful:
    """
    Printful API class. Initializes the connection to the API server.

    :param ck: Consumer Key.
    :param cs: Consumer Secret.
    :returns: A stateful object with an authenticated connection.
    """
    VERSION = "1.0.0a3"

    _store = {
        'base_url': 'https://api.printful.com/',
        'connection': None,
        'auth': None,
        'last_response': None,
        'last_response_raw': None,
        'consumer_key': None,
        'consumer_secret': None,
    }

    def __init__(self, ck=None, cs=None, connect=True):
        if not (ck and cs):
            raise pfException("Please provide a valid API Key.")
        self._store.consumer_key = ck
        self._store.consumer_secret = cs
        if connect:
            self.connect()
        return True

    def connect(self):
        self._store.connection = requests.Session()
        self._store.connection.auth = HTTPBasicAuth(
            self._store.consumer_key, self._store.consumer_secret)
        self._store.connection.headers['User-Agent'] = "pyPrintful (Printful API Wrapper for Python 3)"
        self._store.connection.headers['Content-Type'] = 'application/json'
        return True

    def get_product_list(self):
        """Get all product list"""
        raise NotImplementedError()

    def get_variant_info(self, pk=None):
        """Get info about a variant"""
        raise NotImplementedError()

    def get_product_info(self, pk=None):
        """Get product’s variant list"""
        raise NotImplementedError()

    def get_order_list(self):
        """Get order list"""
        raise NotImplementedError()

    def put_order_new(self):
        """Create new order"""
        raise NotImplementedError()

    def get_order_info(self, pk=None):
        """Get order data"""
        raise NotImplementedError()

    def put_order_cancel(self, pk=None):
        """Cancel an order"""
        raise NotImplementedError()

    def put_order_update(self, pk=None):
        """Update order data"""
        raise NotImplementedError()

    def put_order_confirm(self, pk=None):
        """Confirm draft for fulfillment"""
        raise NotImplementedError()

    def get_file_list(self):
        raise NotImplementedError()

    def put_file_new(self):
        raise NotImplementedError()

    def get_file_info(self, pk=None):
        raise NotImplementedError()

    def get_shippingrate_calc(self):
        raise NotImplementedError()

    def get_syncproduct_list(self):
        raise NotImplementedError()

    def get_syncproduct_info(self, pk=None):
        raise NotImplementedError()

    def put_syncproduct_remove(self, pk=None):
        raise NotImplementedError()

    def get_syncvariant_info(self, pk=None):
        raise NotImplementedError()

    def get_countries_list(self):
        raise NotImplementedError()

    def get_tax_geos(self):
        raise NotImplementedError()

    def get_tax_calc(self):
        raise NotImplementedError()

    def get_webhooks_info(self):
        raise NotImplementedError()

    def put_webhooks_update(self):
        raise NotImplementedError()

    def put_webhooks_disable(self):
        raise NotImplementedError()

    def get_store_info(self):
        raise NotImplementedError()

    def put_store_packingslip(self):
        raise NotImplementedError()

    def _item_count(self):
        # Returns total available item count from the last request if it supports
        # paging (e.g order list) or nil otherwise
        if(self._store.last_response and 'paging' in self._store.last_response):
            return self._store.last_response['paging']['total']
        else:
            None

    def do_get(self, path, params=None):
        # Perform a GET request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # params - Additional GET parameters as a dictionary
        return self.__request('GET', path, params)

    def do_delete(self, path, params=None):
        # Perform a DELETE request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # params - Additional GET parameters as a dictionary
        return self.__request('DELETE', path, params)

    def do_post(self, path, data=None, params=None):
        # Perform a POST request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # data - Request body data as a dictionary
        # params - Additional GET parameters as a dictionary
        return self.__request('POST', path, params, data)

    def do_put(self, path, data=None, params=None):
        # Perform a PUT request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # data - Request body data as a dictionary
        # params - Additional GET parameters as a dictionary
        return self.__request('PUT', path, params, data)

    def __request(self, method, path, params=None, data=None):
        # Internal generic request wrapper

        self._store.last_response = None
        self._store.last_response_raw = None

        # Allow full URIs in requests. If only providing the route/endpoint, then
        # pre-pend the base_url.
        if path.startswith('http'):
            url = path
        else:
            url = self._store.base_url + path

        if(params):
            url += "?" + urlencode(params)

        if data:
            body = json.dumps(data)
        else:
            body = None

        # Make the request
        try:
            request = self._store.connection.request(
                method,
                url,
                data=body,
            )
            self._store.last_response_raw = request
        except Exception as e:
            raise wcException('API request failed: %s' % e)

        if (self._store.last_response_raw.status_code < 200 or self._store.last_response_raw.status_code >= 300):
            raise pfException('Invalid API response')

        # Now try to decode everything.
        try:
            data = json.loads(
                self._store.last_response_raw.content.decode('utf-8'))
            self._store.last_response = data
        except ValueError as e:
            raise pfException('API response was not valid JSON.')

        return data['result']

    def __defaultvalue(self, value, default_value):
        if value:
            return value
        return default_value
