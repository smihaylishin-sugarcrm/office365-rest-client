from ..services import OnlineMeetingRecordingsService, OnlineMeetingTranscriptsService
from .services_collection import ServicesCollection

class OnlineMeetingServicesCollection(ServicesCollection):
    """
    Wrap a collection of online meeting services in a context.
    """
    def __init__(self, client, prefix):
        super().__init__(client, prefix)
        self.recordings = OnlineMeetingRecordingsService(self.client, self.prefix)
        self.transcripts = OnlineMeetingTranscriptsService(self.client, self.prefix)
