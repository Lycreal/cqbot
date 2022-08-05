import asyncio
from typing import Optional

import pytest
from nonebot.adapters.onebot.v11 import Bot, Message

from .message import handle_group_message
from .utils import MockResponse


@pytest.mark.asyncio
async def test_setu(bot, monkeypatch):
    async def mock_get(self, url, **kwargs):
        return MockResponse(url)

    async def mock_post(self, url, **kwargs):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        m.setattr('httpx.AsyncClient.post', mock_post)

        await handle_group_message(bot, '一张色图')
        respond: Message = (await bot.fetch())['message']
        assert 'base64' in respond[0].data['file']

        respond = await bot.fetch()
        assert respond == {'message_id': 123}
