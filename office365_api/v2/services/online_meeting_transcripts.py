from typing import Any, Dict, Tuple

from .base import BaseService


class OnlineMeetingTranscriptsService(BaseService):
    base_path = 'transcripts'

    def list(self) -> Tuple[Dict[str, Any], str]:
        path = self.base_path
        method = 'get'
        resp = self.execute_request(method, path)
        next_link = resp.get('@odata.nextLink')
        return resp, next_link

    def get(self, transcript_id: str) -> Dict[str, Any]:
        path = f'{self.base_path}/{transcript_id}'
        method = 'get'
        return self.execute_request(method, path)

    def get_content(self, transcript_id: str, transcript_format: str = 'text/vtt') -> bytes:
        path = f'{self.base_path}/{transcript_id}/content'
        method = 'get'
        return self.execute_request(method, path, query_params={'$format': transcript_format}, parse_json_result=False)
