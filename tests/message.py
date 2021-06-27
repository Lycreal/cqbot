from datetime import datetime
from typing import Union, Dict, Any

from nonebot.adapters.cqhttp.bot import Bot

group_id = 111111
user_id = 222222


class NewNumber:
    _self_id = 330000
    _message_id = 1

    @classmethod
    def self_id(cls) -> int:
        cls._self_id += 1
        return cls._self_id

    @classmethod
    def message_id(cls) -> int:
        cls._message_id += 1
        return cls._message_id


# https://github.com/howmanybots/onebot/blob/master/v11/specs/event/message.md#%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF
def generate_private_message(self_id: Union[int, str], message: str) -> Dict[str, Any]:
    return {
        "time": int(datetime.now().timestamp()),
        "self_id": int(self_id),
        "post_type": "message",
        "message_type": "private",
        "sub_type": "friend",
        "message_id": NewNumber.message_id(),
        "user_id": user_id,
        "message": message,
        "raw_message": message,
        "font": 0,
        "sender": {
            "user_id": user_id,
            "nickname": "nickname"
        }
    }


# https://github.com/howmanybots/onebot/blob/master/v11/specs/event/message.md#%E7%BE%A4%E6%B6%88%E6%81%AF
def generate_group_message(self_id: Union[int, str], message: str) -> Dict[str, Any]:
    return {
        "time": int(datetime.now().timestamp()),
        "self_id": int(self_id),
        "post_type": "message",
        "message_type": "group",
        "sub_type": "normal",
        "message_id": NewNumber.message_id(),
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


async def handle_private_message(bot: Bot, message: str) -> None:
    return await bot.handle_message(generate_private_message(bot.self_id, message))


async def handle_group_message(bot: Bot, message: str) -> None:
    return await bot.handle_message(generate_group_message(bot.self_id, message))
