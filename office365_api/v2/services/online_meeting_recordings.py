from typing import Any, Dict, Tuple

from .base import BaseService


class OnlineMeetingRecordingsService(BaseService):
    base_path = 'recordings'

    def list(self) -> Tuple[Dict[str, Any], str]:
        path = self.base_path
        method = 'get'
        resp = self.execute_request(method, path)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, recording_id: str) -> Dict[str, Any]:
        path = f'{self.base_path}/{recording_id}'
        method = 'get'
        return self.execute_request(method, path)

    def get_content(self, recording_id: str) -> bytes:
        path = f'{self.base_path}/{recording_id}/content'
        method = 'get'
        return self.execute_request(method, path, parse_json_result=False)
