from ..services import MasterCategoriesService
from .services_collection import ServicesCollection

class OutlookServicesCollection(ServicesCollection):
    """Wrap a collection of services grouped by 'outlook' context."""
    def __init__(self, client, prefix):
        super().__init__(client, prefix + '/outlook')
        self.masterCategories = MasterCategoriesService(self.client, self.prefix)
