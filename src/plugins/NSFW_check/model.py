import abc
from typing import Dict, Any, Union, Tuple

import httpx
from pydantic import BaseModel


class NSFWChecker(BaseModel):
    async def check_image(self, image: Union[str, bytes]) -> Tuple[int, str]:
        """
        :return: level (0:safe, 1:adult), description (str)
        """

        # always use POST method
        if isinstance(image, str):
            async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
                resp = await client.get(image)
                image_bytes: bytes = await resp.aread()

        response = await self.call_api(image_bytes)
        result = await self.resolve_result(response)
        return result

    @abc.abstractmethod
    async def call_api(self, image: Union[str, bytes]) -> Dict[str, Any]:
        return NotImplemented

    @abc.abstractmethod
    async def resolve_result(self, body: Dict[str, Any]) -> Tuple[int, str]:
        """
        :return: level (0:safe, 1:adult), description (str)
        """
        return NotImplemented
