import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .config import channel_list_cc
from .__init__ import circle, send_to_groups

GROUPS = [GROUP_TST]

channels_cc = [monitor.init_channel('cc', *channel) for channel in channel_list_cc]
vc = circle(len(channels_cc))


@nonebot.scheduler.scheduled_job('interval', seconds=300)
async def _():
    if channels_cc:
        channel = channels_cc[next(vc)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
