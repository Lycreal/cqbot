import nonebot
from nonebot import CommandSession
from plugins.live_monitor import Monitor
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import send_to_groups, channel_list_bili, channel_list_cc, channel_list_you

# import re

__plugin_name__ = '直播监控'
__plugin_usage__ = r'''feature: 直播监控
关键词：monitor
例：monitor command
command list: help, add, del, list, list on, list all
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


@nonebot.scheduler.scheduled_job('interval', seconds=300)
async def monitor_cc_run():
    await send_to_groups(*monitor_cc.run())


monitor_you = Monitor('you')
monitor_you.load()
[monitor_you.add(cid, name, [GROUP_TST, GROUP_BTR]) for cid, name in channel_list_you]
monitor_you.save()


@nonebot.scheduler.scheduled_job('interval', seconds=17)
async def monitor_you_run():
    await send_to_groups(*monitor_you.run())


monitors = {'bili': monitor_bili,
            'cc': monitor_cc,
            'you': monitor_you}


@nonebot.on_command('monitor', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text
    argv = arg.split()
    try:
        cmd = argv[0]
        if cmd == 'add':
            assert len(argv) in [3, 4]
            channel_type = argv[1]
            channel_id = argv[2]
            if len(argv) == 4:
                channel_name = argv[3]
            else:
                channel_name = ''
            ret = monitors[channel_type].add(channel_id, channel_name, session.ctx['group_id'])
            monitors[channel_type].save()
            if ret == 0:
                await session.send(f'已存在：{channel_id} {channel_name}')
            else:
                await session.send(f'已添加：{channel_id} {channel_name}')

        elif cmd == 'del':
            channel_type = argv[1]
            channel_id = argv[2]
            monitors[channel_type].remove(channel_id)

        elif cmd == 'list':
            final_msg = ''
            for monitor in monitors.values():
                msg = ''
                for ch in monitor.channel_list:
                    if session.ctx['group_id'] in ch.sendto:
                        if len(argv) == 1:
                            msg += f'{ch.name}\n'
                        elif len(argv) >= 2 and argv[1] == 'on' and ch.live_status == '1':
                            msg += f'{ch.name}\n'
                        elif argv[1] == 'all':
                            msg += f'{ch.cid}:{ch.name}\n'
                        else:
                            await session.send(str(argv))
                if msg:
                    final_msg += f'{monitor.channel_type}\n'
                    final_msg += msg
            await session.send(final_msg)

        elif cmd == 'help':
            sub = argv[1]
            if sub == 'add':
                await session.send('monitor add [type] [cid] [name]')
            elif sub == 'del':
                await session.send('monitor add [type] [cid]')
            elif sub == 'list':
                msg = 'monitor list\n'
                msg += 'monitor list on\n'
                msg += 'monitor list all'
                await session.send(msg)
        else:
            raise AssertionError

    except (AssertionError, IndexError):
        msg = '''monitor [command]
command list: help, add, del, list, list on, list all'''
        await session.send(msg)
