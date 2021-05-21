import pytest
import json

from model import UvicornTestServer, websocket, event_loop

from message import generate_private_message, generate_group_message


@pytest.mark.usefixtures('event_loop')
@pytest.mark.usefixtures('websocket')
class TestPlugins:
    @pytest.mark.timeout(20)
    def test_search_pic(self, websocket, event_loop):
        msg = f'搜图 [CQ:image,url=https://pixiv.cat/89937761.jpg]'

        event_loop.run_until_complete(websocket.send(json.dumps(generate_group_message(msg))))
        respond = event_loop.run_until_complete(websocket.recv())
        api_call: dict = json.loads(respond)

        assert api_call['action'] == 'send_msg'
        assert any('pixiv' in message['data']['text'] for message in api_call['params']['message'] if message['type'] == 'text')

    @pytest.mark.timeout(20)
    def test_cat(self, websocket, event_loop):
        event_loop.run_until_complete(websocket.send(json.dumps(generate_private_message('猫猫'))))
        respond = event_loop.run_until_complete(websocket.recv())
        api_call: dict = json.loads(respond)

        assert api_call['action'] == 'send_msg'
        assert any(message['type'] == 'image' for message in api_call['params']['message'])
