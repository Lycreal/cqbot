from .message import generate_group_message

from .utils import MockResponse


def test_cat(websocket, monkeypatch):
    async def mock_get(self, url):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)
        websocket.send_json(generate_group_message(websocket.self_id, '猫猫'))
        respond = websocket.receive_json()

    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']

    assert f'base64://{MockResponse.image_base64.decode()}' == [
        message['data']['file']
        for message in respond['params']['message'] if message['type'] == 'image'
    ][0]
