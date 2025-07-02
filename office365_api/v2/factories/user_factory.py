from .base_factory import BaseFactory
from ..collections import UserServicesCollection

class UserServicesFactory(BaseFactory):
    def __call__(self, user_id):
        self.user_id = user_id
        if user_id == 'me':
            return UserServicesCollection(self.client, 'me')
        else:
            return UserServicesCollection(self.client, 'users/' + user_id)
