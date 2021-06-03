from .message import generate_private_message, generate_group_message
from .utils import MockResponse

def test_search_pic(websocket, monkeypatch):
    async def mock_get(self, url):
        return MockResponse(url)

    with monkeypatch.context() as m:
        m.setattr('httpx.AsyncClient.get', mock_get)

        websocket.send_json(generate_private_message(websocket.self_id, '搜上图'))
        respond = websocket.receive_json()
        assert any('未找到上一张图片' in message['data']['text']
                   for message in respond['params']['message'] if message['type'] == 'text')

        msg = f'搜图 [CQ:image,url=https://pixiv.cat/89937761.jpg]'
        websocket.send_json(generate_private_message(websocket.self_id, msg))
        respond = websocket.receive_json()
        assert any('pixiv' in message['data']['text']
                   for message in respond['params']['message'] if message['type'] == 'text')

        websocket.send_json(generate_group_message(websocket.self_id, '[CQ:image,url=https://pixiv.cat/89937761.jpg]'))
        websocket.send_json(generate_group_message(websocket.self_id, '搜上图'))
        respond = websocket.receive_json()
        assert any('pixiv' in message['data']['text']
                   for message in respond['params']['message'] if message['type'] == 'text')
