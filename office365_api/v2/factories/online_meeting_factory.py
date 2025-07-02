from .base_factory import BaseFactory
from ..collections import OnlineMeetingServicesCollection

class OnlineMeetingServicesFactory(BaseFactory):
    def __init__(self, client, prefix):
        super().__init__(client)
        self._prefix = prefix

    def __call__(self, meeting_id: str) -> OnlineMeetingServicesCollection:
        return OnlineMeetingServicesCollection(self.client, f'{self._prefix}/onlineMeetings/{meeting_id}')
