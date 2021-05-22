import pytest

from .message import generate_private_message, generate_group_message
from .utils import websocket


# @pytest.mark.timeout(20)
# def test_cat(websocket):
#     websocket.send_json(generate_private_message('猫猫'))
#     respond = websocket.receive_json()
#
#     # print([message['data']['text'] for message in respond['params']['message'] if message['type'] == 'text'])
#
#     assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
#     assert any(message['type'] in ['text', 'image'] for message in respond['params']['message'])


@pytest.mark.timeout(20)
def test_search_pic(websocket):
    msg = f'搜图 [CQ:image,url=https://pixiv.cat/89937761.jpg]'
    websocket.send_json(generate_group_message(msg))

    respond = websocket.receive_json()
    assert respond['action'] in ['send_msg', 'send_private_msg', 'send_group_msg']
    assert any('pixiv' in message['data']['text']
               for message in respond['params']['message'] if message['type'] == 'text')
