from typing import List, Dict, Any, Union
from datetime import datetime, timedelta

import httpx
from pydantic import BaseModel, validator

from .config import plugin_config
from .model import SetuData, SetuDatabase

data_path = plugin_config.data_path
setu_apikey = plugin_config.setu_apikey
setu_proxy = plugin_config.setu_proxy
setu_r18 = plugin_config.setu_r18


class SetuResp(BaseModel):
    code: int
    msg: str
    quota: int = 0
    quota_min_ttl: int = 0
    time_to_recover: datetime = None
    count: int = 0
    data: List[SetuData] = []

    @validator('time_to_recover', pre=True, always=True)
    def get_ttr(cls, _: datetime, values: Dict[str, Any]) -> datetime:
        quota_min_ttl: int = values['quota_min_ttl']
        return datetime.now() + timedelta(seconds=quota_min_ttl)

    def save(self) -> None:
        SetuDatabase.save(*self.data)

    @staticmethod
    async def get(keyword: str = '') -> "SetuResp":
        api_url = 'https://api.lolicon.app/setu/'
        params: Dict[str, Union[int, str]] = {
            "apikey": setu_apikey,
            "r18": setu_r18,
            "keyword": keyword,
            "num": 10,
            "proxy": setu_proxy,
            "size1200": 'false'
        }
        async with httpx.AsyncClient(timeout=10) as client:  # type: httpx.AsyncClient
            response = await client.get(api_url, params=params)
            content = await response.aread()
        resp: SetuResp = SetuResp.parse_raw(content)
        resp.save()
        return resp
