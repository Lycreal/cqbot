import pytest

from .message import generate_private_message, generate_group_message


@pytest.mark.timeout(30)
def test_search_pic(websocket):
    msg = f'搜图 [CQ:image,url=https://pixiv.cat/89937761.jpg]'
    websocket.send_json(generate_group_message(websocket.self_id, msg))

    respond = websocket.receive_json()
    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any('pixiv' in message['data']['text']
               for message in respond['params']['message'] if message['type'] == 'text')
