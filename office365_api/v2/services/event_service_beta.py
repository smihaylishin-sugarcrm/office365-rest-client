from .base_beta import BaseBetaService

class EventServiceBeta(BaseBetaService):
    def get(self, event_id, params=None, path=None, fields=None):
        fields = fields or []
        if not path:
            path = '/events/'
        path += event_id
        if params is None:
            params = {}
        if fields:
            params['$select'] = ','.join(fields)
        method = 'get'
        return self.execute_request(method, path, query_params=params)
