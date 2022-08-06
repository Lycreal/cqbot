from typing import Union

from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, MessageEvent
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.log import logger

from src.custon_events import MessageSentEvent


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
    if event.get_type() not in ["message", "message_sent"]:
        return False

    event: Union[MessageEvent, MessageSentEvent]
    state['img_urls'] = [
        msg.data['url'] for msg in event.get_message() if msg.type == 'image'
    ]
    logger.info(f'img_urls: {state["img_urls"]}')
    return bool(state['img_urls'])
