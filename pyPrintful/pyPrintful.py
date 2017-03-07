from decimal import Decimal
import json
import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth


class pyPrintful:
    """
    Printful API class. Initializes the connection to the API server.

    :param ck: Consumer Key.
    :param cs: Consumer Secret.
    :returns: A stateful object with an authenticated connection.
    """
    VERSION = "1.0.0a2"

    _storeObj = None
    _connection = None
    _base_url = "https://api.printful.com/"
    _auth = None
    _last_response = None
    _last_response_raw = None

    def __init__(self, ck=None, cs=None):
        if not (ck and cs):
            raise pfException("Please provide a valid API Key.")
        self.connection = requests.Session()
        self.connection.auth = HTTPBasicAuth(
            self._consumer_key, self._consumer_secret)
        self.connection.headers['User-Agent'] = "pyPrintful (Printful API Wrapper for Python 3)"
        self.connection.headers['Content-Type'] = 'application/json'

    def product_list(self):
        """Get all product list"""
        raise NotImplementedError()

    def variant_info(self, pk=None):
        """Get info about a variant"""
        raise NotImplementedError()

    def product_info(self, pk=None):
        """Get product’s variant list"""
        raise NotImplementedError()

    def order_list(self):
        """Get order list"""
        raise NotImplementedError()

    def order_new(self):
        """Create new order"""
        raise NotImplementedError()

    def order_info(self, pk=None):
        """Get order data"""
        raise NotImplementedError()

    def order_cancel(self, pk=None):
        """Cancel an order"""
        raise NotImplementedError()

    def order_update(self, pk=None):
        """Update order data"""
        raise NotImplementedError()

    def order_confirm(self, pk=None):
        """Confirm draft for fulfillment"""
        raise NotImplementedError()

    def file_list(self):
        raise NotImplementedError()

    def file_new(self):
        raise NotImplementedError()

    def file_info(self, pk=None):
        raise NotImplementedError()

    def shippingrate_calc(self):
        raise NotImplementedError()

    def syncproduct_list(self):
        raise NotImplementedError()

    def syncproduct_info(self, pk=None):
        raise NotImplementedError()

    def syncproduct_remove(self, pk=None):
        raise NotImplementedError()

    def syncvariant_info(self, pk=None):
        raise NotImplementedError()

    def countries_list(self):
        raise NotImplementedError()

    def tax_geos(self):
        raise NotImplementedError()

    def tax_calc(self):
        raise NotImplementedError()

    def webhooks_info(self):
        raise NotImplementedError()

    def webhooks_update(self):
        raise NotImplementedError()

    def webhooks_disable(self):
        raise NotImplementedError()

    def store_info(self):
        raise NotImplementedError()

    def store_packingslip(self):
        raise NotImplementedError()

    def _item_count(self):
        # Returns total available item count from the last request if it supports
        # paging (e.g order list) or nil otherwise
        if(self.last_response and 'paging' in self.last_response):
            return self.last_response['paging']['total']
        else:
            None

    def _get(self, path, params=None):
        # Perform a GET request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # params - Additional GET parameters as a dictionary
        return self.__request('GET', path, params)

    def _delete(self, path, params=None):
        # Perform a DELETE request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # params - Additional GET parameters as a dictionary
        return self.__request('DELETE', path, params)

    def _post(self, path, data=None, params=None):
        # Perform a POST request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # data - Request body data as a dictionary
        # params - Additional GET parameters as a dictionary
        return self.__request('POST', path, params, data)

    def _put(self, path, data=None, params=None):
        # Perform a PUT request to the API
        # path - Request path (e.g. 'orders' or 'orders/123')
        # data - Request body data as a dictionary
        # params - Additional GET parameters as a dictionary
        return self.__request('PUT', path, params, data)

    def __request(self, method, path, params=None, data=None):
        # Internal generic request wrapper

        self.last_response = None
        self.last_response_raw = None

        # Allow full URIs in requests. If only providing the route/endpoint, then
        # pre-pend the base_url.
        if path.startswith('http'):
            url = path
        else:
            url = self.base_url + path

        if(params):
            url += "?" + urlencode(params)

        if data:
            body = json.dumps(data)
        else:
            body = None

        # Make the request
        try:
            request = self.connection.request(
                method,
                url,
                # auth=self.auth,
                data=body,
            )
            self.last_response_raw = request
        except Exception as e:
            raise wcException('API request failed: %s' % e)

        if (self.last_response_raw.status_code < 200 or self.last_response_raw.status_code >= 300):
            raise pfException('Invalid API response')

        # Now try to decode everything.
        try:
            data = json.loads(
                self.last_response_raw.content.decode('utf-8'))
            self.last_response = data
        except ValueError as e:
            raise pfException('API response was not valid JSON.')

        return data['result']

    def __defaultvalue(self, value, default_value):
        if value:
            return value
        return default_value
