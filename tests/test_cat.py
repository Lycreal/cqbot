import pytest
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .message import handle_group_message
from .utils import MockResponse


@pytest.mark.asyncio
async def test_cat(bot, monkeypatch) -> None:
    async def mock_get(self, url):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        await handle_group_message(bot, '猫猫')
        respond: Message = (await bot.fetch())['message']
    seg: MessageSegment = respond[0]
    assert seg.type == 'image'
    assert seg.data['file'] == f'base64://{MockResponse.image_base64.decode()}'
