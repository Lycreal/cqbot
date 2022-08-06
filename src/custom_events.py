from nonebot.adapters.onebot.v11.event import MessageEvent, PrivateMessageEvent, GroupMessageEvent
from typing_extensions import Literal


class MessageSentEvent(MessageEvent):
    post_type: Literal["message_sent"]
