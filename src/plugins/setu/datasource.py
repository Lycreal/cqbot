from typing import List, Dict, Union

import httpx
from pydantic import BaseModel

from .config import plugin_config
from .model import SetuData, SetuDatabase

setu_proxy = plugin_config.setu_proxy
setu_r18 = plugin_config.setu_r18


class SetuResp(BaseModel):
    code: int
    msg: str
    count: int = 0
    data: List[SetuData] = []

    def save(self) -> None:
        SetuDatabase.save(*self.data)

    @staticmethod
    async def get(keyword: str = '') -> "SetuResp":
        # doc: https://api.lolicon.app/#/setu?id=api
        api_url = 'https://api.lolicon.app/setu/'
        params: Dict[str, Union[int, str]] = {
            "r18": setu_r18,
            "keyword": keyword,
            "num": 10,
            "proxy": setu_proxy,
            "size1200": 'true'
        }
        async with httpx.AsyncClient(timeout=10) as client:  # type: httpx.AsyncClient
            response = await client.get(api_url, params=params)
            content = await response.aread()
        resp: SetuResp = SetuResp.parse_raw(content)
        resp.save()
        return resp
