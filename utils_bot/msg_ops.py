from nonebot import get_bot

bot = get_bot()
SUPERUSERS = bot.config.SUPERUSERS
MY_NAMES = bot.config.NICKNAME.union({'机器人', '复读机'})


async def send_to_superusers(msg: str):
    for eachId in SUPERUSERS:
        await bot.send_private_msg(user_id=eachId, message=msg)


async def send_to_groups(groups, msg: str):
    for groupId in groups:
        await bot.send_group_msg(group_id=groupId, message=str(msg).strip())


def msg_is_calling_me(msg: str) -> bool:
    for myName in MY_NAMES:
        if myName in msg:
            return True
    return False
