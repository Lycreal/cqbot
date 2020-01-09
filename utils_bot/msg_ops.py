from nonebot import get_bot
from nonebot.log import logger
from config_bot import SUPERUSERS, NICKNAME

MY_NAMES = NICKNAME.union({'机器人', '复读机', 'Bot', 'bot'})


async def send_to_superusers(msg: str):
    for eachId in SUPERUSERS:
        await get_bot().send_private_msg_rate_limited(user_id=eachId, message=msg)


async def send_to_groups(groups: list, msg: str):
    logger.debug(str((groups, msg)))
    if msg:
        for groupId in groups:
            await get_bot().send_group_msg_rate_limited(group_id=groupId, message=str(msg).strip())


def msg_is_calling_me(msg: str) -> bool:
    for myName in MY_NAMES:
        if myName in msg:
            return True
    return False
