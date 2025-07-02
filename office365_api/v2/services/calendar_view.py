from .base import BaseService

class CalendarViewService(BaseService):
    def list(self, start_datetime, end_datetime, max_entries=50, _filter='', calendar_id=None):
        path = ''
        if calendar_id:
            path = '/calendars/%s' % calendar_id
        path += '/calendarView'
        method = 'get'
        query_params = {
            'startDateTime': start_datetime,
            'endDateTime': end_datetime,
            '$top': max_entries
        }
        if _filter:
            query_params['$filter'] = _filter
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def delta_list(self, start_datetime=None, end_datetime=None, delta_token=None, calendar_id=None, max_entries=50):
        path = ''
        if calendar_id:
            path = '/calendars/%s' % calendar_id
        path += '/calendarView/delta'
        method = 'get'
        headers = {
            'Prefer': 'odata.maxpagesize=%d' % max_entries
        }
        query_params = {}
        if not delta_token:
            query_params.update({
                'startDateTime': start_datetime,
                'endDateTime': end_datetime,
            })
        else:
            query_params.update({
                '$deltaToken': delta_token,
            })
        resp = self.execute_request(
            method, path, query_params=query_params, headers=headers)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link
