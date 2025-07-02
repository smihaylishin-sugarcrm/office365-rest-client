import json

from .base import BaseService


class MailFolderService(BaseService):
    def create(self, **kwargs):
        path = '/mailFolders'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)

    def list(self, max_entries=50):
        path = '/mailFolders'
        method = 'get'
        query_params = {'$top': max_entries}
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def delta_list(self, folder_id, delta_token=None, _filter=None, max_entries=50, fields=None):
        fields = fields or []
        path = '/mailFolders/{}/messages/delta'.format(folder_id)
        method = 'get'
        headers = {
            'Prefer': 'odata.maxpagesize=%d' % max_entries
        }
        query_params = {}
        if delta_token:
            query_params.update({'$deltaToken': delta_token})
        if _filter:
            query_params.update({'$filter': _filter})
        if fields:
            query_params.update({'$select': ','.join(fields)})
        resp = self.execute_request(method, path, query_params=query_params, headers=headers)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, folder_id):
        path = '/mailFolders/' + folder_id
        method = 'get'
        return self.execute_request(method, path)

    def list_childfolders(self, folder_id, max_entries=50):
        path = '/mailFolders/' + folder_id + '/childFolders'
        method = 'get'
        query_params = {'$top': max_entries}
        resp = self.execute_request(method, path, query_params=query_params)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def create_childfolder(self, folder_id, **kwargs):
        path = '/mailFolders/' + folder_id + '/childFolders'
        method = 'post'
        body = json.dumps(kwargs)
        return self.execute_request(method, path, body=body)
