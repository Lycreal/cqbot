from nonebot import on_natural_language, NLPSession
from nonebot.permission import IS_PRIVATE
from utils_bot.msg_ops import send_to_superusers


# 将收到的私聊信息转发给管理者


@on_natural_language(permission=IS_PRIVATE)
async def _(session: NLPSession):
    # if session.ctx['sub_type'] in ['group', 'discuss']:
    await send_to_superusers(repr(session.ctx))
