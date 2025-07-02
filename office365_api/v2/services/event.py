import json
from typing import Any, Dict

from .base import BaseService


class EventService(BaseService):
    def create(self, calendar_id=None, **kwargs):
        if calendar_id:
            path = '/calendars/' + calendar_id + '/events'
        else:
            path = '/calendar/events'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def list(self, calendar_id=None, _filter='', max_entries=50):
        if calendar_id:
            path = '/calendars/' + calendar_id + '/events'
        else:
            path = '/calendar/events'
        method = 'get'
        query_params: Dict[str, Any] = {
            "$top": max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, event_id, params=None, path=None):
        if not path:
            path = '/calendar/events/'
        path += event_id
        method = 'get'
        return self.execute_request(method, path, query_params=params)

    def update(self, event_id, path=None, **kwargs):
        if not path:
            path = '/calendar/events/'
        path += event_id
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def delete(self, event_id, path=None):
        if not path:
            path = '/calendar/events/'
        path += event_id
        method = 'delete'
        return self.execute_request(method, path)
