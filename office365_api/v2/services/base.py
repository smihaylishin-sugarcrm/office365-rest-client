import logging
import urllib.parse

from requests import HTTPError
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from ..consts import (DEFAULT_MAX_ENTRIES, RESPONSE_FORMAT_ODATA,
                      RESPONSE_FORMAT_RAW, RETRIES_COUNT)
from ..exceptions import (Office365ClientError, Office365QuotaExceededError,
                          Office365ServerError)

logger = logging.getLogger(__name__)


class BaseService(object):
    base_url = 'https://graph.microsoft.com'
    graph_api_version = 'v1.0'
    supported_response_formats = [RESPONSE_FORMAT_ODATA, RESPONSE_FORMAT_RAW]

    def __init__(self, client, prefix):
        self.client = client
        self.prefix = prefix

    def build_url(self, path):
        if path.startswith('/'):
            path = path.lstrip('/')
        path_parts = [self.base_url, self.graph_api_version, self.prefix, path]
        return '/'.join(s for s in path_parts if s)

    def follow_next_link(self, next_link, max_entries=DEFAULT_MAX_ENTRIES, fields=None):
        fields = fields or []
        full_prefix = '%s/%s/%s' % (self.base_url, self.graph_api_version, self.prefix)
        _, _, path = next_link.partition(full_prefix)
        headers = {'Prefer': 'odata.maxpagesize=%d' % max_entries}
        query_params = {"$select": ','.join(fields)} if fields else None
        resp = self.execute_request('get', path, query_params=query_params, headers=headers)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def execute_request(self, method, path, query_params=None, headers=None, body=None, parse_json_result=True, set_content_type=True):
        full_url = self.build_url(path)
        if query_params:
            querystring = urllib.parse.urlencode(query_params)
            full_url += '?' + querystring
        if set_content_type:
            default_headers = {'Content-Type': 'application/json'} if parse_json_result else {'Content-Type': 'text/html'}
        else:
            default_headers = {}
        if headers:
            default_headers.update(headers)
        logger.info('{}: {}'.format(method.upper(), full_url))
        retries = RETRIES_COUNT
        while True:
            try:
                resp = self.client.session.request(url=full_url, method=method.upper(), data=body, headers=default_headers)
                if parse_json_result:
                    try:
                        return resp.json()
                    except RequestsJSONDecodeError:
                        return resp.content
                else:
                    return resp.content
            except HTTPError as e:
                if e.response.status_code < 500:
                    try:
                        error_data = e.response.json()
                    except (ValueError, RequestsJSONDecodeError):
                        error_data = {'error': {'message': e.response.content, 'code': 'unknown'}}
                    if e.response.status_code == 429:
                        retry_after = None
                        try:
                            retry_after = int(
                                e.response.headers.get('Retry-After'))
                        except Exception as ex:
                            logger.error(
                                'Error parsing Retry-After header: %s', ex)
                        raise Office365QuotaExceededError(
                            data=error_data, retry_after=retry_after) from e
                    raise Office365ClientError(e.response.status_code, error_data) from e
                else:
                    raise Office365ServerError(e.response.status_code, e.response.content) from e
            except (ConnectionResetError, RequestsConnectionError, ChunkedEncodingError, ):
                retries -= 1
                if retries == 0:
                    raise
