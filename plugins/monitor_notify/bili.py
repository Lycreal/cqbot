import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .config import channel_list_bili
from .__init__ import circle, send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR, GROUP_KR]

channels_bili = [monitor.init_channel('bili', *channel) for channel in channel_list_bili]
vb = circle(len(channels_bili))


@nonebot.scheduler.scheduled_job('interval', seconds=5)
async def _():
    if channels_bili:
        channel = channels_bili[next(vb)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
