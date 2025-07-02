

from ..services import (CalendarService,
                        CalendarViewService,
                        EventService,
                        EventServiceBeta,
                        MessageService,
                        AttachmentService,
                        ContactFolderService,
                        ContactService,
                        MailFolderService,
                        UserService,
                        MailboxSettingsService,
                        OnlineMeetingService)

from ..collections.services_collection import ServicesCollection
from ..collections.outlook_services_collection import OutlookServicesCollection


class UserServicesCollection(ServicesCollection):
    """Wrap a collection of services in a context."""
    def __init__(self, client, prefix):
        super().__init__(client, prefix)
        self.calendar = CalendarService(self.client, self.prefix)
        self.calendarview = CalendarViewService(self.client, self.prefix)
        self.event = EventService(self.client, self.prefix)
        self.event_beta = EventServiceBeta(self.client, self.prefix)
        self.message = MessageService(self.client, self.prefix)
        self.attachment = AttachmentService(self.client, self.prefix)
        self.contactfolder = ContactFolderService(self.client, self.prefix)
        self.contact = ContactService(self.client, self.prefix)
        self.mailfolder = MailFolderService(self.client, self.prefix)
        self.user = UserService(self.client, self.prefix)
        self.mailboxSettings = MailboxSettingsService(self.client, self.prefix)
        self.outlook = OutlookServicesCollection(self.client, self.prefix)
        self.onlineMeeting = OnlineMeetingService(self.client, self.prefix)
        from ..factories.online_meeting_factory import OnlineMeetingServicesFactory
        self.onlineMeetings = OnlineMeetingServicesFactory(self.client, self.prefix)
