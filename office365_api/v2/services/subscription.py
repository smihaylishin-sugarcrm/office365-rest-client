import base64
import json
from datetime import datetime
from typing import List

from .base import BaseService


class SubscriptionService(BaseService):
    """
    Service for managing Microsoft Teams change notification subscriptions for call recordings and transcripts.
    See: https://learn.microsoft.com/en-us/graph/teams-changenotifications-callrecording-and-calltranscript
    """
    def create(self, resource: str, change_type: List[str], notification_url: str, expiration_datetime: datetime,
               client_state: str | None = None, include_resource_data: bool = False, encryption_certificate: bytes | None = None,
                encryption_certificate_id: str | None = None, lifecycle_notification_url: str | None = None, **kwargs)->dict:
        path = 'subscriptions'
        method = 'post'
        body: dict = {
            "changeType": ','.join(change_type),
            "notificationUrl": notification_url,
            "resource": resource,
            "expirationDateTime": expiration_datetime.isoformat(),
        }
        if client_state:
            body["clientState"] = client_state
        if include_resource_data:
            if not encryption_certificate or not encryption_certificate_id:
                raise ValueError(
                    "encryption_certificate and encryption_certificate_id are required when include_resource_data is True")
            body["includeResourceData"] = True
            body["encryptionCertificate"] = base64.b64encode(
                encryption_certificate).decode("ascii")
            body["encryptionCertificateId"] = encryption_certificate_id
        if lifecycle_notification_url:
            body["lifecycleNotificationUrl"] = lifecycle_notification_url
        body.update(kwargs)
        return self.execute_request(method, path, body=json.dumps(body))

    def renew(self, subscription_id: str, expiration_datetime: datetime):
        path = f'subscriptions/{subscription_id}'
        method = 'patch'
        body = {
            "expirationDateTime": expiration_datetime.isoformat()
        }
        return self.execute_request(method, path, body=json.dumps(body))

    def delete(self, subscription_id: str):
        path = f'subscriptions/{subscription_id}'
        method = 'delete'
        return self.execute_request(method, path)
