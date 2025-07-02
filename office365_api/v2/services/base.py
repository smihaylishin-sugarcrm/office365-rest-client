import urllib.parse
import logging
from requests import HTTPError
from requests.exceptions import ChunkedEncodingError, ConnectionError as RequestsConnectionError, JSONDecodeError as RequestsJSONDecodeError

from ..exceptions import Office365ClientError, Office365ServerError
from ..consts import DEFAULT_MAX_ENTRIES, RETRIES_COUNT, RESPONSE_FORMAT_ODATA, RESPONSE_FORMAT_RAW

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
                    raise Office365ClientError(e.response.status_code, error_data) from e
                else:
                    raise Office365ServerError(e.response.status_code, e.response.content) from e
            except (ConnectionResetError, RequestsConnectionError, ChunkedEncodingError, ):
                retries -= 1
                if retries == 0:
                    raise
