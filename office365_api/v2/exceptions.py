# -* -coding: utf-8 -*-
import json


class Office365ClientError(Exception):

    def __init__(self, status_code: int = 0, data: dict | None = None, error_message: str | None = None):
        self.status_code = status_code
        data = data or {}
        self.error_code = data.get('error', {}).get('code', '')
        self.error_message = error_message or data.get('error', {}).get('message', '')
        super(Office365ClientError, self).__init__('{}: {}: {}'.format(
            status_code,
            self.error_code,
            self.error_message))

    @property
    def is_invalid_tokens(self):
        # The refresh_token has expired. Ask to re-login
        return self.status_code == 400

    @property
    def is_invalid_session(self):
        # Need to use refresh_token
        return self.status_code == 401

    @property
    def is_forbidden(self):
        return self.status_code == 403

    @property
    def is_not_found(self):
        return self.status_code == 404

    @property
    def is_expired_sync_token(self):
        return (self.error_code or '').lower() == 'syncstatenotfound'

    def __repr__(self):
        return '<{0}>: {1} {2} ({3})'.format(
            'Office365ClientError', self.status_code, self.error_code, self.error_message)


class Office365QuotaExceededError(Office365ClientError):
    '''
    Exception raised when quota limit is exceeded (HTTP status code 429).
    Attributes:
        data -- error data returned by the server
        error_message -- explanation of the error returned by the server
        retry_after -- time in seconds to wait before retrying the request
    '''

    def __init__(self, data=None, error_message=None, retry_after: str | int | None = None):

        super(Office365QuotaExceededError, self).__init__(
            status_code=429, data=data, error_message=error_message)
        self.retry_after = retry_after

class Office365ServerError(Exception):

    def __init__(self, status_code, body):
        super(Office365ServerError, self).__init__(
            '{}: {}'.format(status_code, body))
        self.status_code = status_code
        try:
            data = json.loads(body)
            self.error_code = data['error']['code']
        except:
            self.error_code = ''

        self.error_message = body

    @property
    def is_response_timeout(self):
        # request takes too long to complete
        return self.status_code in [503, 504] and self.error_code == 'UnknownError'
