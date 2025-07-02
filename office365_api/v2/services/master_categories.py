import json

from .base import BaseService


class MasterCategoriesService(BaseService):
    def list(self, max_entries=50):
        path = '/masterCategories'
        method = 'get'
        query_params = {'$top': max_entries}
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def create(self, **kwargs):
        path = '/masterCategories'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def get(self, category_id):
        path = '/masterCategories/' + category_id
        method = 'get'
        return self.execute_request(method, path)

    def update(self, category_id, **kwargs):
        path = '/masterCategories/' + category_id
        method = 'patch'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def delete(self, category_id):
        path = '/masterCategories/' + category_id
        method = 'delete'
        return self.execute_request(method, path)
