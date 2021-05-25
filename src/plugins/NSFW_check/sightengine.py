from typing import Dict, Any
from urllib.parse import quote

import httpx

from .model import NSFWChecker


# https://sightengine.com/docs/nsfw-detection-model
class SightEngineClient(NSFWChecker):
    api_user: str
    api_secret: str
    threshold: float = 0.5
    api_url: str = 'https://api.sightengine.com/1.0/check.json'

    async def call_api(self, image_url: str) -> Dict[str, Any]:
        params = {
            'models': 'nudity',
            'api_user': self.api_user,
            'api_secret': self.api_secret,
            'url': quote(image_url)
        }
        async with httpx.AsyncClient(timeout=10) as client:  # type: httpx.AsyncClient
            resp = await client.get(self.api_url, params=params)
            respond: Dict[str, Any] = await resp.json()
        return respond

    async def resolve_result(self, body: Dict[str, Any]) -> float:
        safe: float = body['nudity']['safe']
        return safe
