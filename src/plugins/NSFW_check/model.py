import abc
import asyncio
from json import dumps
from typing import Dict, Any, Union, Tuple, List

import httpx
from nonebot import logger
from pydantic import BaseModel


class NSFWChecker(BaseModel):
    name: str

    async def check_image(self, image: Union[str, bytes]) -> Tuple[int, str]:
        """
        :return: level (0:safe, 1:adult), description (str)
        """

        # always use POST method
        if isinstance(image, str):
            async with httpx.AsyncClient(timeout=30) as client:  # type: httpx.AsyncClient
                resp = await client.get(image)
                image_bytes: bytes = await resp.aread()
        else:
            image_bytes = image
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


class NSFWMultiChecker(List[NSFWChecker]):
    async def check_image(self, image: Union[str, bytes]) -> Tuple[int, str]:
        tasks = []
        for checker in self:
            tasks.append(asyncio.create_task(checker.check_image(image), name=checker.name))

        done, pending = await asyncio.wait(tasks, timeout=10)

        results: Dict[str, Tuple[int, str]] = {
            task.get_name(): task.result()
            for task in done if not task.cancelled() and not task.exception()
        }

        result = int(all(result[0] for result in results.values()))  # 有0得0，全1得1
        description = dumps(results)

        logger.info(f"NSFW检查：{result}，详情：{description}")

        return result, description
