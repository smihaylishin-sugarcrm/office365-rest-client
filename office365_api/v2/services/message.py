import json
from typing import Any, Dict

from .base import BaseService


class MessageService(BaseService):
    def list(self, _filter=None, _search=None, max_entries=50, fields=None):
        fields = fields or []
        path = '/messages'
        method = 'get'
        query_params: Dict[str, Any] = {
            "$top": max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        if _search:
            query_params['$search'] = _search
        if fields:
            query_params['$select'] = ','.join(fields)
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, message_id, _filter=None, format='odata'):
        if format not in self.supported_response_formats:
            raise ValueError(format)
        if format == 'odata':
            path = '/messages/{}'.format(message_id)
        elif format == 'raw':
            path = '/messages/{}/$value'.format(message_id)
        else:
            raise NotImplementedError(format)
        method = 'get'
        return self.execute_request(method, path, query_params=_filter, parse_json_result=(not format == 'raw'))

    def create(self, **kwargs):
        path = '/messages'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def send(self, message_id, **kwargs):
        path = '/messages/{}/send'.format(message_id)
        method = 'post'
        return self.execute_request(method, path, headers={'Content-Length': '0'}, set_content_type=False, parse_json_result=False)

    def update(self, message_id, **kwargs):
        path = '/messages/{}'.format(message_id)
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def move(self, message_id, destination_id):
        path = '/messages/{}/move'.format(message_id)
        method = 'post'
        body = json.dumps({'DestinationId': destination_id})
        return self.execute_request(method, path, body=body)
