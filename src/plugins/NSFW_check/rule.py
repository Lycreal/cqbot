from nonebot import Bot
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Message
from nonebot.typing import T_State


async def contain_image(bot: "Bot", event: "Event", state: T_State) -> bool:
    if event.get_type() not in ["message", "message_sent"]:
        return False

    blacklist = ['(直播)', '(动态)']
    if any(word in msg for msg in Message(event.message) for word in blacklist):
        return False

    # noinspection Mypy, PyUnresolvedReferences
    state['img_urls'] = [
        msg.data['url'] for msg in Message(event.message) if msg.type == 'image'
    ]
    return bool(state['img_urls'])
