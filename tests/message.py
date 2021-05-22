from datetime import datetime

group_id = 111111
user_id = 222222
self_id = 333333
_message_id = 1


def message_id():
    global _message_id
    _message_id += 1
    return _message_id


# https://github.com/howmanybots/onebot/blob/master/v11/specs/event/message.md#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
def generate_private_message(message: str):
    return {
        "time": int(datetime.now().timestamp()),
        "self_id": self_id,
        "post_type": "message",
        "message_type": "private",
        "sub_type": "friend",
        "message_id": message_id(),
        "group_id": group_id,
        "user_id": user_id,
        "anonymous": None,
        "message": message,
        "raw_message": message,
        "font": 0,
        "sender": {
            "user_id": user_id,
            "nickname": "nickname"
        }
    }


# https://github.com/howmanybots/onebot/blob/master/v11/specs/event/message.md#%E7%BE%A4%E6%B6%88%E6%81%AF
def generate_group_message(message: str):
    return {
        "time": int(datetime.now().timestamp()),
        "self_id": self_id,
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": message_id(),
        "group_id": group_id,
        "user_id": user_id,
        "anonymous": None,
        "message": message,
        "raw_message": message,
        "font": 0,
        "sender": {
            "user_id": user_id,
            "nickname": "nickname"
        }
    }
