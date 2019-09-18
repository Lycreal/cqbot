# import plugins.live_monitor as monitor
import nonebot
# from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .config import *


def circle(n):
    x = 0
    while True:
        yield x
        x = x + 1 if x < n - 1 else 0


bot = nonebot.get_bot()


# GROUPS = [GROUP_TST, GROUP_BTR, GROUP_KR]


async def send_to_groups(GROUPS: list, msg: str):
    for groupId in GROUPS:
        await bot.send_group_msg(group_id=groupId, message=msg)
