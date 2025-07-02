import json
from typing import Any, Dict, List, Tuple

from .base import BaseService


class ContactFolderService(BaseService):
    def list(self, max_entries=50):
        path = '/contactFolders'
        method = 'get'
        query_params = {
            '$top': max_entries
        }
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, folder_id):
        path = '/contactFolders/' + folder_id
        method = 'get'
        return self.execute_request(method, path)

    def create(self, **kwargs):
        path = '/contactFolders'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def delta_list(self, folder_id: str = 'contacts', fields: List[str] = [], delta_token: str | None = None, max_entries=50) -> Tuple[Dict[str, Any], str]:
        path = f"/contactFolders('{folder_id}')/contacts/delta"
        method = 'get'
        query_params = None
        if delta_token:
            query_params = {
                '$deltatoken': delta_token
            }
        elif fields:
            query_params = {
                '$select': ','.join(fields)
            }
        headers = {
            'Prefer': 'odata.maxpagesize=%d' % max_entries
        }
        resp = self.execute_request(method, path, query_params=query_params, headers=headers)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link
