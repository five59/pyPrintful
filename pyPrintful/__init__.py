from decimal import Decimal
import json
import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth


class pyPrintful:
    """
    Printful API class. Initializes the connection to the API server.

    :param key: API Key (Get it from your store's dashboard). Note that this
        is not the consumer key and secret found under store info. Rather,
        the API key can be found under Store > API and will be two strings
        separated by a ':'.
    :returns: A stateful object with an authenticated connection.
    """

    VERSION = "1.0.0"

    _store = {
        'base_url': 'https://api.printful.com/',
        'connection': None,
        'auth': None,
        'last_response': None,
        'last_response_raw': None,
        'auth_user': None,
        'auth_pass': None,
    }

    def __init__(self, key=None, connect=True):
        if not key:
            raise pfException("Please provide a valid API Key.")

        self._store['auth_user'], self._store['auth_pass'] = key.split(
            ':')
        if connect:
            self.connect()

    def connect(self):
        """
        Configures the connection to the remote server.
        """
        self._store['connection'] = requests.Session()
        self._store['connection'].auth = HTTPBasicAuth(
            self._store['auth_user'], self._store['auth_pass'])
        self._store['connection'].headers[
            'User-Agent'] = "pyPrintful (Printful API Wrapper for Python 3)"
        self._store['connection'].headers['Content-Type'] = 'application/json'

    def get_product_list(self):
        """
        Get all product list
        """
        return self.do_get('products')

    def get_variant_info(self, pk=None):
        """
        Get info about a variant

        :param pk: The Printful identifier for the variant.
        """
        return self.do_get('products/variant/' + pk)

    def get_product_info(self, pk=None):
        """
        Get product's variant list

        :param pk: The Printful identifier for the variant.
        """
        return self.do_get('products/' + pk)

    def get_order_list(self):
        """
        Get order list
        """
        return self.do_get('orders')

    def put_order_new(self, data=None):
        """
        Create new order
        """
        return self.do_post("orders", data=data)

    def get_order_info(self, pk=None):
        """
        Get order data
        """
        return self.do_get('orders/' + pk)

    def put_order_cancel(self, pk=None):
        """
        Cancel an order
        """
        return self.do_delete("orders/" + pk)

    def put_order_update(self, pk=None, data=None):
        """
        Update order data
        """
        return self.do_put("orders/" + pk, data=data)

    def put_order_confirm(self, pk=None):
        """
        Confirm draft for fulfillment
        """
        return self.do_post('orders/' + pk + "/confirm")

    def get_file_list(self):
        """
        Get list of files
        """
        return self.do_get('files')

    def put_file_new(self, data):
        """
        Add new file
        """
        return self.do_post('/files', data=data)

    def get_file_info(self, pk=None):
        """
        Get file info
        """
        return self.do_get('files/' + pk)

    def get_shippingrate_calc(self, data):
        """
        Calculate shipping rates
        """
        return self.do_post("shipping/rates", data=data)

    def get_syncproduct_list(self):
        """
        Get list of sync products
        """
        return self.do_get('sync/products')

    def get_syncproduct_info(self, pk=None):
        """
        Get info about sync product
        """
        return self.do_get('sync/products/' + pk)

    def put_syncproduct_remove(self, pk=None):
        """
        Unlink all synced variants of this product
        """
        return self.do_delete('sync/products/' + pk)

    def get_syncvariant_info(self, pk=None):
        """
        Get info about sync variant
        """
        return self.do_get('sync/variant/' + pk)

    def get_countries_list(self):
        """
        Retrieve country list
        """
        return self.do_get('countries')

    def get_tax_geos(self):
        """
        Retrieve state list that requires state tax calc
        """
        return self.do_get('tax/rates')

    def get_tax_calc(self, data=None):
        """
        Calculate tax rate
        """
        return self.do_post("tax/rates", data=data)

    def get_webhooks_info(self):
        """
        Get webhook configuration
        """
        return self.do_get('webhooks')

    def put_webhooks_update(self, data=None):
        """
        Set up webhook configuration
        """
        return self.do_post("webhooks", data=data)

    def put_webhooks_disable(self):
        """
        Disable webhook support. No data param, because the API doesn't
        require it.
        """
        return self.do_delete("webhooks")

    def get_store_info(self):
        """
        Get store info
        """
        return self.do_get('store')

    def put_store_packingslip(self, data=None):
        """
        Change store packing slip
        """
        return self.do_post('store/packing-slip', data=data)

    def get_item_count(self):
        """
        Returns total available item count from the last request if it supports
        paging (e.g order list) or nil otherwise
        """
        if(self._store['last_response'] and 'paging' in self._store['last_response']):
            return self._store['last_response']['paging']['total']
        else:
            None

    def do_get(self, path, params=None):
        """
        Perform a GET request to the API

        :param path: Request path (e.g. 'orders' or 'orders/123')
        :param params: Additional GET parameters as a dictionary
        """
        return self.__request('GET', path, params)

    def do_delete(self, path, params=None):
        """
        Perform a DELETE request to the API

        :param path: Request path (e.g. 'orders' or 'orders/123')
        :param params: Additional GET parameters as a dictionary
        """
        return self.__request('DELETE', path, params)

    def do_post(self, path, data=None, params=None):
        """
        Perform a POST request to the API

        :param path: Request path (e.g. 'orders' or 'orders/123')
        :param data: Request body data as a dictionary
        :param params: Additional GET parameters as a dictionary
        """
        return self.__request('POST', path, params, data)

    def do_put(self, path, data=None, params=None):
        """
        Perform a PUT request to the API

        :param path: Request path (e.g. 'orders' or 'orders/123')
        :param data: Request body data as a dictionary
        :param params: Additional PUT parameters as a dictionary
        """
        return self.__request('PUT', path, params, data)

    def __request(self, method, path, params=None, data=None):
        """
        Internal generic request wrapper

        :param method:
        :param path:
        :param params:
        :param data:
        """
        self._store['last_response'] = None
        self._store['last_response_raw'] = None

        # Allow full URIs in requests. If only providing the route/endpoint,
        # then pre-pend the base_url.
        if path.startswith('http'):
            url = path
        else:
            url = self._store['base_url'] + path

        if(params):
            url += "?" + urlencode(params)

        if data:
            body = json.dumps(data)
        else:
            body = None

        # Make the request
        try:
            request = self._store['connection'].request(
                method,
                url,
                data=body,
            )
            self._store['last_response_raw'] = request
        except Exception as e:
            raise wcException('API request failed: %s' % e)

        if (self._store['last_response_raw'].status_code < 200 or self._store['last_response_raw'].status_code >= 300):
            raise pfException('Invalid API response')

        # Now try to decode everything.
        try:
            data = json.loads(
                self._store['last_response_raw'].content.decode('utf-8'))
            self._store['last_response'] = data
        except ValueError as e:
            raise pfException('API response was not valid JSON.')

        return data['result']

    def __defaultvalue(self, value, default_value):
        if value:
            return value
        return default_value


class pfException(Exception):
    """Printful exception returned from the API."""
    pass


class pfAPIException(pfException):
    """API Exception Class"""

    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code
        self.message = message

    def __str__(self):
        return '%i - %s' % (self.code, self.message)
