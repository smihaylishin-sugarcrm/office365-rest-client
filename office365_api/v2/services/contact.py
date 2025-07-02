import json
from typing import Any, Dict

from .base import BaseService


class ContactService(BaseService):
    def create(self, contact_folder_id=None, **kwargs):
        if contact_folder_id:
            path = '/contactFolders/' + contact_folder_id + '/contacts'
        else:
            path = '/contacts'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def list(self, contact_folder_id=None, _filter='', max_entries=50):
        if contact_folder_id:
            path = '/contactFolders/' + contact_folder_id + '/contacts'
        else:
            path = '/contacts'
        method = 'get'
        query_params: Dict[str, Any] = {
            "$top": max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, contact_id):
        path = '/contacts/' + contact_id
        method = 'get'
        return self.execute_request(method, path)

    def delete(self, contact_id):
        path = '/contacts/' + contact_id
        method = 'delete'
        return self.execute_request(method, path)

    def update(self, contact_id, **kwargs):
        path = '/contacts/' + contact_id
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)
