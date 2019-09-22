import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_you
from .utils import circle, send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR]

channels_you = [monitor.init_channel('you', *channel) for channel in channel_list_you]
vy = circle(len(channels_you))


@nonebot.on_command('monitor_you_status', only_to_me=False)
async def monitor_you_status(session: nonebot.CommandSession):
    msg = ''
    for ch in channels_you:
        msg += str(ch)
    await session.send(msg)


@nonebot.scheduler.scheduled_job('interval', seconds=20)
async def monitor_you():
    if channels_you:
        channel = channels_you[next(vy)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
