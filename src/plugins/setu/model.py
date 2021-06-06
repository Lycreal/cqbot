import json
from pathlib import Path
from typing import Any
from typing import List, Set
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel, ValidationError

from .config import plugin_config

data_path = plugin_config.data_path
setu_proxy = plugin_config.setu_proxy
setu_r18 = plugin_config.setu_r18

Path(data_path).mkdir(exist_ok=True)
SAVE_FILE = Path(data_path).joinpath('setu.json')


class SetuData(BaseModel):
    pid: int = None
    p: int = None
    uid: int = None
    title: str = None
    author: str = None
    url: str
    r18: bool = None
    width: int = None
    height: int = None
    tags: List[str] = []

    @property
    def purl(self) -> str:
        return 'https://www.pixiv.net/artworks/{}'.format(Path(urlparse(self.url).path).stem.split('_')[0])

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.url == other.url
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.url)

    def save(self) -> None:
        """保存至文件"""
        SetuDatabase.save(self)

    async def get(self) -> bytes:
        """从网络获取图像"""
        headers = {'Referer': 'https://www.pixiv.net/'} if 'i.pximg.net' in self.url else {}
        async with httpx.AsyncClient(headers=headers, timeout=10) as client:  # type: httpx.AsyncClient
            response: httpx.Response = await client.get(self.url)
            img_bytes: bytes = await response.aread()
        return img_bytes


class SetuDatabase(BaseModel):
    __root__: Set[SetuData] = set()

    @classmethod
    def load_from_file(cls) -> "SetuDatabase":
        try:
            db: SetuDatabase = cls.parse_file(SAVE_FILE)
        except (FileNotFoundError, json.JSONDecodeError, ValidationError):
            db = cls()
        return db

    def save_to_file(self) -> None:
        with SAVE_FILE.open('w', encoding='utf8') as f:
            json.dump([data.dict() for data in self.__root__], f, ensure_ascii=False, indent=2)

    @classmethod
    def save(cls, *data_array: SetuData) -> None:
        db: SetuDatabase = cls.load_from_file()
        for data in data_array:
            db.__root__.discard(data)
            db.__root__.add(data)
        db.save_to_file()
