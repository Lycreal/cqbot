import abc
from typing import Dict, Any

from pydantic import BaseModel


class NSFWChecker(BaseModel):
    async def check_image(self, image_url: str) -> float:
        response = await self.call_api(image_url)
        result = await self.resolve_result(response)
        return result

    @abc.abstractmethod
    async def call_api(self, image_url: str) -> Dict[str, Any]:
        return NotImplemented

    @abc.abstractmethod
    async def resolve_result(self, body: Dict[str, Any]) -> float:
        return NotImplemented
