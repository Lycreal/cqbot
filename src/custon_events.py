from nonebot.adapters.onebot.v11.event import MessageEvent
from typing_extensions import Literal


class MessageSentEvent(MessageEvent):
    post_type: Literal["message_sent"]
