import logging

from requests import HTTPError
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from office365_api.v2.exceptions import (Office365ClientError,
                                         Office365ServerError)

from .base import BaseService

logger = logging.getLogger(__name__)

class BatchService(BaseService):
    def __init__(self, client, beta=True):
        self.client = client
        channel = 'beta' if beta else 'v1.0'
        self.batch_uri = f'https://graph.microsoft.com/{channel}/$batch'
        self._callbacks = {}
        self._requests = {}
        self._order = []
        self._last_auto_id = 0
        self._responses = {}

    def _new_id(self):
        self._last_auto_id += 1
        while str(self._last_auto_id) in self._requests:
            self._last_auto_id += 1
        return str(self._last_auto_id)

    def add(self, request, callback=None):
        request_id = self._new_id()
        self._requests[request_id] = request
        self._callbacks[request_id] = callback
        self._order.append(request_id)

    def _execute(self, requests):
        if self.is_empty:
            raise Office365ClientError(error_message='No requests to execute in a batch')
        method = 'POST'
        default_headers = {'Content-Type': 'application/json'}
        logger.info('{}: {} with {}x requests'.format(
            method, self.batch_uri, len(requests)))
        try:
            resp = self.client.session.request(
                url=self.batch_uri,
                method=method,
                json={'requests': requests},
                headers=default_headers)
            return resp.json()
        except HTTPError as e:
            if e.response.status_code < 500:
                try:
                    error_data = e.response.json()
                except (ValueError, RequestsJSONDecodeError):
                    error_data = {
                        'error': {'message': e.response.content, 'code': 'unknown'}}
                raise Office365ClientError(e.response.status_code, error_data)
            else:
                raise Office365ServerError(
                    e.response.status_code, e.response.content)

    def execute(self):
        requests = []
        for request_id in self._order:
            request = self._requests[request_id]
            request['id'] = request_id
            requests.append(request)
        responses = self._execute(requests)
        for resp in responses['responses']:
            self._responses[resp['id']] = resp
        for request_id in self._order:
            response = self._responses[request_id]
            request = self._requests[request_id]
            callback = self._callbacks[request_id]
            exception = None
            try:
                if response['status'] >= 300:
                    error_data = response.get('body')
                    raise Office365ClientError(response['status'], error_data)
            except Office365ClientError as e:
                exception = e
            if callback is not None:
                callback(request_id, response['body'], exception)

    @property
    def is_empty(self) -> bool:
        return not self._order
