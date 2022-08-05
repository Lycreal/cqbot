import pytest
from nonebot.adapters.onebot.v11 import Message

from .message import handle_private_message
from .utils import MockResponse


@pytest.mark.asyncio
async def test_search_pic(bot, monkeypatch):
    async def mock_get(self, url):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)

        await handle_private_message(bot, '搜上图')
        respond: Message = (await bot.fetch())['message']
        assert respond.extract_plain_text() == '未找到上一张图片'

        await handle_private_message(bot, '[CQ:image,url=https://pixiv.cat/89937761.jpg]')
        await handle_private_message(bot, '搜上图')
        respond = (await bot.fetch())['message']
        assert 'pixiv' in respond.extract_plain_text()

        msg = f'搜图 [CQ:image,url=https://pixiv.cat/89937761.jpg]'
        await handle_private_message(bot, msg)
        respond = (await bot.fetch())['message']
        assert 'pixiv' in respond.extract_plain_text()
