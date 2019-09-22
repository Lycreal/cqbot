from plugins.live_monitor import Monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_bili
from .utils import send_to_groups

GROUPS = [GROUP_TST]

monitor = Monitor('bili')
monitor.load()
[monitor.add(id, name) for id, name in channel_list_bili]
monitor.save()


@nonebot.on_command('monitor_bili2_status', only_to_me=False)
async def monitor_bili2_status(session: nonebot.CommandSession):
    await session.send(str(monitor).strip())


@nonebot.scheduler.scheduled_job('interval', seconds=14)
async def monitor_bili_alter():
    await send_to_groups(GROUPS, str(monitor.run()))
