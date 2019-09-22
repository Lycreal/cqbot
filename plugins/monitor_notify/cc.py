from plugins.live_monitor import Monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_cc
from .utils import send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR]

monitor = Monitor('cc')
monitor.load()
[monitor.add(cid, name) for cid, name in channel_list_cc]
monitor.save()


@nonebot.on_command('monitor_cc_status', only_to_me=False)
async def monitor_cc_status(session: nonebot.CommandSession):
    await session.send(str(monitor).strip())


@nonebot.scheduler.scheduled_job('interval', seconds=600)
async def monitor_cc():
    await send_to_groups(GROUPS, str(monitor.run()))
