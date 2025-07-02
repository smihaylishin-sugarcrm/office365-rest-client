import json
import urllib.parse

def become_request(self, method, path, query_params=None, headers=None, body=None, parse_json_result=True):
    """
    Batch Request to JSON.

    Patches the execute_request() to not fire the http request. Instead,
    force to return a json data of the request for batch processing.
    """
    default_headers = {'Content-Type': 'application/json'}
    if headers:
        default_headers.update(headers)

    request = {
        'method': method.upper(),
        'headers': default_headers,
    }
    if body:
        # Reverse the json dump
        body = json.loads(body)
        request['body'] = body

    if path.startswith('/'):
        path = path.lstrip('/')

    if self.prefix:
        path = '/%s/%s' % (self.prefix, path)

    url = path
    if query_params:
        qs = urllib.parse.urlencode(query_params)
        url += '?' + qs

    request.update({'url': url})
    return request
