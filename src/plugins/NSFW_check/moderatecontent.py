import json
from io import BytesIO
from typing import Dict, Any, Union, Tuple

import httpx

from .model import NSFWChecker


# https://moderatecontent.com/documentation/anime
class ModerateContentClient(NSFWChecker):
    name: str = 'ModerateContent'

    api_key: str
    api_url: str = 'https://api.moderatecontent.com/moderate/'

    async def call_api(self, image: Union[str, bytes]) -> Dict[str, Any]:
        if isinstance(image, str):
            return await self.call_api_get(image)
        else:
            return await self.call_api_post(image)

    async def call_api_get(self, image_url: str) -> Dict[str, Any]:
        params = {
            'key': self.api_key,
            'url': image_url.replace('://i.pximg.net', '://i.pixiv.cat', 1)
        }
        async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
            resp = await client.get(self.api_url, params=params)
            respond: Dict[str, Any] = resp.json()
        return respond

    async def call_api_post(self, image_bytes: bytes) -> Dict[str, Any]:
        data = {'key': self.api_key}
        files = {'file': BytesIO(image_bytes)}
        async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
            resp = await client.post(self.api_url, data=data, files=files)
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
