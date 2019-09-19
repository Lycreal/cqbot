import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_you
from .utils import circle, send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR]

channels_you = [monitor.init_channel('you', *channel) for channel in channel_list_you]
vy = circle(len(channels_you))


@nonebot.scheduler.scheduled_job('interval', seconds=40)
async def _():
    if channels_you:
        channel = channels_you[next(vy)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
