from plugins.live_monitor import Monitor
import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import channel_list_you
from .utils import send_to_groups

GROUPS = [GROUP_TST, GROUP_BTR]

monitor = Monitor('you')
monitor.load()
[monitor.add(cid, name) for cid, name in channel_list_you]
monitor.save()


@nonebot.on_command('monitor_you_status', only_to_me=False)
async def monitor_you_status(session: nonebot.CommandSession):
    await session.send(str(monitor).strip())


@nonebot.scheduler.scheduled_job('interval', seconds=19)
async def monitor_you():
    await send_to_groups(GROUPS, str(monitor.run().strip()))
