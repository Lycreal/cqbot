from os import environ
from queue import Empty

import pytest

from .message import generate_group_message


@pytest.mark.xfail(environ.get('CI') == 'true', reason='fail for github actions, reason unknown', raises=Empty)
def test_cat(websocket):
    websocket.send_json(generate_group_message(websocket.self_id, '猫猫'))
    respond = websocket.receive_json()

    # print([message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text'])

    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any(message['type'] in ['text', 'image'] for message in respond['params']['message'])
