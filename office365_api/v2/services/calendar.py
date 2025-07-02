import json
from typing import Any, Dict

from .base import BaseService


class CalendarService(BaseService):
    def list(self, _filter='', max_entries=50):
        path = '/calendars'
        method = 'get'
        query_params: Dict[str, Any] = {
            "$top": max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, calendar_id=None):
        if calendar_id:
            path = '/calendars/' + calendar_id
        else:
            path = '/calendar'
        method = 'get'
        return self.execute_request(method, path)

    def create(self, **kwargs):
        path = '/calendars'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def delete(self, calendar_id):
        path = '/calendars/' + calendar_id
        method = 'delete'
        return self.execute_request(method, path)

    def update(self, calendar_id, **kwargs):
        path = '/calendars/' + calendar_id
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)
