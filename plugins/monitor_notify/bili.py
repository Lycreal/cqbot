import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_bili
from .utils import circle, send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR, GROUP_KR]

channels_bili = [monitor.init_channel('bili', *channel) for channel in channel_list_bili]
vb = circle(len(channels_bili))


@nonebot.on_command('monitor_bili_status', only_to_me=False)
async def monitor_bili_status(session: nonebot.CommandSession):
    msg = ''
    for ch in channels_bili:
        msg += str(ch)
    await session.send(msg.strip())


@nonebot.scheduler.scheduled_job('interval', seconds=3)
async def monitor_bili():
    if channels_bili:
        channel = channels_bili[next(vb)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
