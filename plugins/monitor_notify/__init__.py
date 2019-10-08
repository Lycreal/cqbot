import nonebot
from nonebot import CommandSession
from plugins.live_monitor import Monitor
from config_private import GROUP_TST, GROUP_BTR, GROUP_KR
from .utils import send_to_groups, channel_list_bili, channel_list_cc, channel_list_you

# import re

__plugin_name__ = '直播监控'
__plugin_usage__ = r'''feature: 直播监控
关键词：monitor [command]
command list: help, add, del, list
例：monitor help
'''
monitors = {'bili': Monitor('bili'),
            'you': Monitor('you'),
            'cc': Monitor('cc')}

monitor_bili = monitors['bili']
monitor_you = monitors['you']
monitor_cc = monitors['cc']

monitor_bili.load()
[monitor.load() for monitor in monitors.values()]
[monitor_bili.add(cid, name, [GROUP_TST, GROUP_BTR, GROUP_KR]) for cid, name in channel_list_bili]
[monitor_you.add(cid, name, [GROUP_TST, GROUP_BTR]) for cid, name in channel_list_you]
[monitor_cc.add(cid, name, [GROUP_TST, GROUP_BTR]) for cid, name in channel_list_cc]
[monitor.save() for monitor in monitors.values()]


@nonebot.scheduler.scheduled_job('interval', seconds=3)
async def monitor_bili_run():
    await send_to_groups(*monitor_bili.run())


@nonebot.scheduler.scheduled_job('interval', seconds=300)
async def monitor_cc_run():
    await send_to_groups(*monitor_cc.run())


@nonebot.scheduler.scheduled_job('interval', seconds=17)
async def monitor_you_run():
    await send_to_groups(*monitor_you.run())


@nonebot.on_command('monitor', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text
    argv = arg.split()
    group = str(session.ctx['group_id'])
    try:
        cmd = argv[0]
        if cmd == 'add':
            channel_type = argv[1]
            channel_id = argv[2]
            if len(argv) == 4:
                channel_name = argv[3]
            else:
                channel_name = ''
            ret = monitors[channel_type].add(channel_id, channel_name, group)
            monitors[channel_type].save()
            if ret == 0:
                await session.send(f'已存在：{channel_id} {channel_name}')
            else:
                await session.send(f'已添加：{channel_id} {channel_name}')

        elif cmd == 'del':
            channel_type = argv[1]
            channel_id = argv[2]
            ret = monitors[channel_type].remove(channel_id, group)
            monitors[channel_type].save()
            if ret:
                await session.send(f'已移除：{channel_id}')
            else:
                await session.send(f'未找到：{channel_id}')

        elif cmd == 'list':
            if len(argv) >= 2:
                sub = argv[1]
            else:
                sub = ''
            final_msg = ''
            for monitor in monitors.values():
                msg = ''
                for ch in monitor.channel_list:
                    if group in ch.sendto:
                        name = ch.name if ch.name else ch.ch_name
                        if sub == '':
                            msg += f'{name}:{ch.live_status}\n'
                        elif sub == 'on' and ch.live_status == '1':
                            msg += f'{name}\n'
                        elif sub == 'all':
                            msg += f'{ch.cid}:{name}\n'
                        else:
                            raise AssertionError
                if msg:
                    final_msg += f'[{monitor.channel_type}]\n'
                    final_msg += msg
            await session.send(final_msg)

        elif cmd == 'help':
            argv.pop(0)
            await help_(session, *argv)
        else:
            await help_(session, *argv)

    except (AssertionError, IndexError):
        await help_(session, *argv)


async def help_(session: CommandSession, *argv):
    msg = ''
    if not argv:
        argv = ['']
    if argv[0] == 'add':
        msg += 'monitor add [type] [cid] [name]\n'
        msg += '[type]:频道类型,备选值:bili,you,cc\n'
        msg += '[cid]:频道id,对于bilibili指直播间号\n'
        msg += '[name]:频道名\n'
        msg += '频道名若不填写，将自动获取'
    elif argv[0] == 'del':
        msg += 'monitor del [type] [cid]\n'
        msg += '[type]:频道类型\n'
        msg += '[cid]:频道id\n'
        msg += '可使用monitor list all查看所有频道'
    elif argv[0] == 'list':
        msg += 'monitor list 查看频道及直播状态\n'
        msg += 'monitor list on 查看正在直播的频道\n'
        msg += 'monitor list all 查看所有频道及频道id\n'
    else:
        msg += 'monitor [command]\n'
        msg += 'command list: help, add, del, list\n'
        msg += '详细帮助（例）：monitor help add\n'
    await session.send(msg.strip())
