import json
from typing import Dict, Any, Union, Tuple

import httpx

from .model import NSFWChecker


# https://moderatecontent.com/documentation/anime
class ModerateContentClient(NSFWChecker):
    api_key: str
    api_url: str = 'https://api.moderatecontent.com/anime/'

    async def call_api(self, image: Union[str, bytes]) -> Dict[str, Any]:
        if isinstance(image, str):
            return await self.call_api_get(image)
        else:
            return NotImplemented

    async def call_api_get(self, image_url: str) -> Dict[str, Any]:
        params = {
            'key': self.api_key,
            'url': image_url
        }
        async with httpx.AsyncClient(timeout=10) as client:  # type: httpx.AsyncClient
            resp = await client.get(self.api_url, params=params)
            respond: Dict[str, Any] = resp.json()
        return respond

    async def resolve_result(self, response: Dict[str, Any]) -> Tuple[int, str]:
        error_code = response.get('error_code')
        if error_code != 0:
            return 0, response.get('error')

        predictions = response.get('predictions')
        rating_label = response.get('rating_label')

        if rating_label == 'adult':
            level = 1
        else:
            level = 0
        return level, json.dumps(predictions)
