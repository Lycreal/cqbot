import abc
from pydantic import BaseModel

import httpx
import PIL.Image
from io import BytesIO
from .config import plugin_config


class PictureSource(BaseModel, abc.ABC):
    @classmethod
    @abc.abstractmethod
    def api_url(cls) -> str:
        return NotImplemented

    @classmethod
    async def get_image(cls) -> bytes:
        content_with_url = await cls.get_content(cls.api_url())
        image_url = await cls.resolve(content_with_url)
        image_bytes = await cls.get_content(image_url)
        PIL.Image.open(BytesIO(image_bytes))
        return image_bytes

    @classmethod
    @abc.abstractmethod
    async def resolve(cls, content: bytes) -> str:
        """
        :param content: content of get(API_URL)
        :return: Image URL
        """
        return NotImplemented

    @staticmethod
    async def get_content(url: str) -> bytes:
        async with httpx.AsyncClient(timeout=plugin_config.cats_api_timeout) as client:  # type: httpx.AsyncClient
            response = await client.get(url)  # type: httpx.Response
            content: bytes = await response.aread()
        return content
