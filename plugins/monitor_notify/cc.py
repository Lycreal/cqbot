import plugins.live_monitor as monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_cc
from .utils import circle, send_to_groups

GROUPS = [GROUP_TST]

channels_cc = [monitor.init_channel('cc', *channel) for channel in channel_list_cc]
vc = circle(len(channels_cc))


@nonebot.on_command('monitor_cc_status', only_to_me=False)
async def monitor_cc_status(session: nonebot.CommandSession):
    msg = ''
    for ch in channels_cc:
        msg += str(ch)
    await session.send(msg)


@nonebot.scheduler.scheduled_job('interval', seconds=300)  # 必须小于TIME_PRE
async def monitor_cc():
    if channels_cc:
        channel = channels_cc[next(vc)]
        if channel.update():
            await send_to_groups(GROUPS, channel.notify())
