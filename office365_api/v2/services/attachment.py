import json
from typing import Any, Dict

from .base import BaseService


class AttachmentService(BaseService):
    def list(self, message_id, _filter=None, fields=[], max_entries=50):
        path = '/messages/{}/attachments'.format(message_id)
        method = 'get'
        query_params: Dict[str, Any] = {
            "$top": max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        if fields:
            query_params['$select'] = ','.join(fields)
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def list_first_page(self, message_id, _filter=None, fields=[]):
        resp, _ = self.list(message_id, _filter, fields)
        return resp

    def get(self, message_id, attachment_id):
        path = '/messages/{}/attachments/{}'.format(message_id, attachment_id)
        method = 'get'
        return self.execute_request(method, path)

    def get_content(self, message_id, attachment_id):
        path = '/messages/{}/attachments/{}/$value'.format(message_id, attachment_id)
        method = 'get'
        return self.execute_request(method, path, parse_json_result=False)

    def create(self, message_id, **kwargs):
        path = '/messages/{}/attachments'.format(message_id)
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)
