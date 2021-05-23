import base64
from os import environ
from queue import Empty

import pytest

from .message import generate_group_message


class MockResponse:
    image_base64 = ''.join("""
    Qk1mAAAAAAAAADYAAAAoAAAABAAAAAQAAAABABgAAAAAAA
    AAAADEDgAAxA4AAAAAAAAAAAAAJBzsJBzsJBzsJBzsJBzs
    APL/APL/JBzsJBzsAPL/APL/JBzsJBzsJBzsJBzsJBzs
    """.split())

    def __init__(self, url):
        self.url = url

    async def aread(self):
        if self.url == "https://api.thecatapi.com/v1/images/search":
            return '[{"url": "https://fakeurl/pic.bmp"}]'
        elif self.url == "https://fakeurl/pic.bmp":
            return base64.b64decode(self.image_base64)
        else:
            raise


def test_cat(websocket, monkeypatch):
    async def mock_get(self, url):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        websocket.send_json(generate_group_message(websocket.self_id, '猫猫'))
        respond = websocket.receive_json()

    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any(
        message['data']['file'] == f'base64://{MockResponse.image_base64}'
        for message in respond['params']['message'] if message['type'] == 'image'
    )
