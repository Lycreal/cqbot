from plugins.live_monitor import Monitor
# import nonebot
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import *

__plugin_name__ = '直播监控'
__plugin_usage__ = r'''feature: 直播监控
查看状态：monitor_bili_status
'''

monitor_bili = Monitor('bili')
monitor_bili.load()
[monitor_bili.add(cid, name, [GROUP_TST, GROUP_BTR, GROUP_KR]) for cid, name in channel_list_bili]
monitor_bili.save()


@nonebot.scheduler.scheduled_job('interval', seconds=3)
async def monitor_bili_run():
    await send_to_groups(*monitor_bili.run())


monitor_cc = Monitor('cc')
monitor_cc.load()
[monitor_cc.add(cid, name, [GROUP_TST, GROUP_BTR]) for cid, name in channel_list_cc]
monitor_cc.save()


@nonebot.scheduler.scheduled_job('interval', seconds=600)
async def monitor_cc_run():
    await send_to_groups(*monitor_cc.run())


monitor_you = Monitor('you')
monitor_you.load()
[monitor_you.add(cid, name, [GROUP_TST, GROUP_BTR]) for cid, name in channel_list_you]
monitor_you.save()


@nonebot.scheduler.scheduled_job('interval', seconds=19)
async def monitor_you_run():
    await send_to_groups(*monitor_you.run())
