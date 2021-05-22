import pytest

from .message import generate_private_message, generate_group_message


@pytest.mark.timeout(30)
def test_setu(websocket):
    websocket.send_json(generate_group_message(websocket.self_id, '色图'))

    respond = websocket.receive_json()

    # print([message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text'])

    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any(message['type'] in ['text', 'image'] for message in respond['params']['message'])
