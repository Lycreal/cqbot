import json
from io import BytesIO
from typing import Dict, Any, Union
from typing import Tuple

import httpx

from .model import NSFWChecker


# https://sightengine.com/docs/reference#nudity-detection
class SightEngineClient(NSFWChecker):
    name: str = 'SightEngine'

    api_user: str
    api_secret: str
    api_url: str = 'https://api.sightengine.com/1.0/check.json'

    async def call_api(self, image: Union[str, bytes]) -> Dict[str, Any]:
        if isinstance(image, str):
            return await self.call_api_get(image)
        else:
            return await self.call_api_post(image)

    async def call_api_get(self, image_url: str) -> Dict[str, Any]:
        params = {
            'models': 'nudity',
            'api_user': self.api_user,
            'api_secret': self.api_secret,
            'url': image_url.replace('://i.pximg.net', '://i.pixiv.cat', 1)
        }
        async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
            resp = await client.get(self.api_url, params=params)
            respond: Dict[str, Any] = resp.json()
        return respond

    async def call_api_post(self, image_bytes: bytes) -> Dict[str, Any]:
        data = {
            'models': 'nudity',
            'api_user': self.api_user,
            'api_secret': self.api_secret
        }
        files = {'media': BytesIO(image_bytes)}
        async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
            resp = await client.post(self.api_url, data=data, files=files)
            respond: Dict[str, Any] = resp.json()
        return respond

    async def resolve_result(self, body: Dict[str, Any]) -> Tuple[int, str]:
        level = 0
        if body['status'] == 'success':
            nudity: Dict[str, float] = body['nudity']
            description = json.dumps(nudity)
            # https://sightengine.com/docs/nsfw-detection-model
            if nudity['raw'] >= max(nudity['partial'], nudity['safe']):
                level = 1
        else:
            description = body['error']['message']
        return level, description
