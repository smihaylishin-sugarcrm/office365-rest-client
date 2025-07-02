import json
from typing import Any, Dict

from .base import BaseService


class OnlineMeetingService(BaseService):
    base_path = 'onlineMeetings'

    def list(self, _filter: str):
        if not _filter:
            raise ValueError("Filter parameter is required for listing online meetings.")
        path = self.base_path
        method = 'get'
        query_params: Dict[str, Any] = {
            "$filter": _filter,
        }
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, meeting_id: str) -> Dict[str, Any]:
        path = f'{self.base_path}/{meeting_id}'
        method = 'get'
        return self.execute_request(method, path)

    def create(self, **kwargs) -> Dict[str, Any]:
        path = self.base_path
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def update(self, meeting_id: str, **kwargs) -> Dict[str, Any]:
        path = f'{self.base_path}/{meeting_id}'
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def delete(self, meeting_id: str) -> Dict[str, Any]:
        path = f'{self.base_path}/{meeting_id}'
        method = 'delete'
        return self.execute_request(method, path)
