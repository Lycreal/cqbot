import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR
from .config import *


def circle(n):
    x = 0
    while True:
        yield x
        x = x + 1 if x < n - 1 else 0


bot = nonebot.get_bot()

GROUPS = [GROUP_TST, GROUP_BTR]


async def send_to_groups(msg: str):
    for groupId in GROUPS:
        await bot.send_group_msg(group_id=groupId, message=msg)


channels_bili = [monitor.init_channel('bili', *channel) for channel in channel_list_bili]
vb = circle(len(channels_bili))


@nonebot.scheduler.scheduled_job('interval', seconds=2.5)
async def _():
    if channels_bili:
        channel = channels_bili[next(vb)]
        if channel.update():
            await send_to_groups(channel.notify())


channels_you = [monitor.init_channel('you', *channel) for channel in channel_list_bili]
vy = circle(len(channels_you))


@nonebot.scheduler.scheduled_job('interval', seconds=30)
async def _():
    if channels_you:
        channel = channels_you[next(vy)]
        if channel.update():
            await send_to_groups(channel.notify())


channels_cc = [monitor.init_channel('cc', *channel) for channel in channel_list_bili]
vc = circle(len(channels_cc))


@nonebot.scheduler.scheduled_job('interval', seconds=300)
async def _():
    if channels_cc:
        channel = channels_cc[next(vc)]
        if channel.update():
            await send_to_groups(channel.notify())
