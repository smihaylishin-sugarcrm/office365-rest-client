from .base import BaseService

class UserService(BaseService):
    def get(self):
        path = ''
        method = 'get'
        resp = self.execute_request(method, path)
        return resp
