from typing import Optional

import pytest
from nonebot.adapters.cqhttp import Bot, Message

from .message import handle_group_message
from .utils import MockResponse


@pytest.mark.asyncio
async def test_NSFW(bot, monkeypatch) -> None:
    async def mock_get(self, url, *args, **kwargs):
        return MockResponse(url)

    async def mock_get_msg(self, *, message_id: int, self_id: Optional[int] = ...):
        return {
            "message_id": 123123,
            "message": "[CQ:image,url=https://pixiv.cat/89910126.png]",
            'time': 123456,
            'message_type': 'group',
            'real_id': 123123,
            'sender': {
                'user_id': 222222
            }
        }

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        m.setattr('httpx.AsyncClient.post', mock_get)
        Bot.get_msg = mock_get_msg

        await handle_group_message(bot, '[CQ:reply,id=123123] 检查')
        respond: Message = (await bot.fetch())['message']

    assert '0.' in respond.extract_plain_text()
