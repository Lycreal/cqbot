from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment
from nonebot.rule import Rule
from nonebot.typing import T_State


def full_match(*keywords: str) -> Rule:
    """
    完全匹配消息关键词

    :param keywords: 关键词
    :return: Rule
    """

    async def _keyword(bot: "Bot", event: "Event", state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        text = event.get_plaintext()

        return bool(text and text.strip() in keywords)

    return Rule(_keyword)


async def contain_image(bot: "Bot", event: "Event", state: T_State) -> bool:
    if event.get_type == 'message':
        state['img_urls'] = [
            msg.data['url'] for msg in event.get_message() if msg.type == 'image'
        ]
    elif event.get_type == 'message_sent':
        state['img_urls'] = [
            msg['data']['url'] for msg in event.message if msg['type'] == 'image'
        ]
    else:
        return False
    return bool(state['img_urls'])
