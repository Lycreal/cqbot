import pytest

from .message import generate_private_message, generate_group_message
from .utils import websocket


@pytest.mark.timeout(40)
def test_cat(websocket):
    # doesn't work for github actions, reason unknown

    websocket.send_json(generate_group_message('猫猫'))
    respond = websocket.receive_json()

    # print([message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text'])

    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any(message['type'] in ['text', 'image'] for message in respond['params']['message'])
