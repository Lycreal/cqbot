from typing import Optional

from nonebot.adapters.cqhttp import Bot

from .message import generate_group_message
from .utils import MockResponse


def test_setu(websocket, monkeypatch):
    async def mock_get(self, url, **kwargs):
        return MockResponse(url)

    async def mock_post(self, url, **kwargs):
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

    async def mock_sleep(*args, **kwargs):
        pass

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        m.setattr('httpx.AsyncClient.post', mock_post)

        Bot.get_msg = mock_get_msg

        websocket.send_json(generate_group_message(websocket.self_id, '一张色图'))
        respond = websocket.receive_json()

        print(''.join(message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text'))
        assert any(message['type'] == 'image' for message in respond['params']['message'])
        websocket.send_json(
            {
                'status': 'ok',
                'retcode': 0,
                'data': {
                    'message_id': 123
                },
                'echo': {
                    'seq': respond['echo']['seq']
                }
            }
        )
        respond = websocket.receive_json()
        assert respond['action'] == 'delete_msg'
