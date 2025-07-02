from .base import BaseService

class MailboxSettingsService(BaseService):
    def get(self):
        path = '/mailboxSettings'
        method = 'get'
        resp = self.execute_request(method, path)
        return resp
