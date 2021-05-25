from typing import Optional

from nonebot.adapters.cqhttp import Bot

from .message import generate_group_message


class MockResponse:
    def __init__(self, url):
        self.url = url

    def json(self):
        if "api.sightengine.com" in self.url:
            return {
                "status": "success",
                "request": {
                    "id": "req_9HisoSsOFwi2r4wtcrWv6",
                    "timestamp": 1621912096.273972,
                    "operations": 1
                },
                "nudity": {
                    "raw": 0.55,
                    "safe": 0.06,
                    "partial": 0.38
                },
                "media": {
                    "id": "med_9Hise8F0KrlCvgwVTjJv4",
                    "uri": "https://pixiv.cat/89910126.png"
                }
            }
        else:
            raise


def test_NSFW(websocket, monkeypatch):
    async def mock_get(self, url, params=None):
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
        Bot.get_msg = mock_get_msg

        websocket.send_json(generate_group_message(websocket.self_id, '[CQ:reply,id=123123] 检查'))
        respond = websocket.receive_json()

    text = ''.join(message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text')
    assert '0.' in text


def test_auto_recall(websocket, monkeypatch):
    async def mock_get(self, url, params=None):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        websocket.send_json({
            "time": 1621927543,
            "self_id": websocket.self_id,
            "post_type": "message_sent",
            "message_type": "group",
            "group_id": 305175005,
            "message": [
                {
                    "data": {
                        "url": "http://pixiv.cat/86398208.png"
                    },
                    "type": "image"
                }
            ],
            "anonymous": None,
            "message_seq": 11665,
            "font": 0,
            "raw_message": "[CQ:image,url=http://pixiv.cat/86398208.png]",
            "sub_type": "normal",
            "user_id": websocket.self_id,
            "sender": {
            },
            "message_id": 2055500411
        })
        respond = websocket.receive_json()
        assert respond['action'] == 'delete_msg'
