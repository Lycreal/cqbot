import nonebot
from nonebot import CommandSession
from .live_monitor import Monitor
from .buffer import buffer
import re

__plugin_name__ = '直播监控'
__plugin_usage__ = r'''直播监控
关键词：monitor [command]
command list: help, add, del, list
例：.monitor help add
'''
monitors = {'bili': Monitor('bili'),
            'you': Monitor('you'),
            'cc': Monitor('cc')}

[monitor.load() for monitor in monitors.values()]


@nonebot.scheduler.scheduled_job('interval', seconds=3)
async def monitor_bili_run():
    monitor = monitors['bili']
    await monitor.run(buffer.input)


@nonebot.scheduler.scheduled_job('interval', seconds=20)
async def monitor_you_run():
    monitor = monitors['you']
    await monitor.run(buffer.input)


@nonebot.scheduler.scheduled_job('interval', seconds=60)
async def monitor_cc_run():
    monitor = monitors['cc']
    await monitor.run(buffer.input)


@nonebot.on_command('monitor', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text
    argv = arg.split()

    try:
        cmd = argv[0]
        if cmd == 'add':
            await add_(session, *argv)
        elif cmd == 'del':
            await del_(session, *argv)
        elif cmd == 'list':
            await list_(session, *argv)
        elif cmd == 'help':
            argv.pop(0)
            await help_(session, *argv)
        else:
            await help_(session, *argv)
    except AssertionError as e:
        await session.send(str(e))
    except (IndexError, TypeError):
        await help_(session, *argv)


async def add_(session: CommandSession, *argv: str):
    group = str(session.ctx['group_id'])
    if argv[1] in ['bili', 'you', 'cc']:
        channel_type = argv[1]
        channel_id = argv[2]
        channel_name = argv[3] if len(argv) >= 4 else ''
    elif argv[1].find('http') != '-1':
        url = argv[1]
        channel_name = argv[2] if len(argv) >= 3 else ''
        if url.find('bilibili') != -1:
            channel_type = 'bili'
            channel_id = re.search(r'live.bilibili.com/(\d+)', url)[1]
        elif url.find('youtube.com') != -1:
            channel_type = 'you'
            channel_id = re.search(r'UC[\w-]{22}', url)[0]
        elif url.find('cc.163.com') != -1:
            channel_type = 'cc'
            channel_id = re.search(r'cc.163.com/(\d+)', url)[1]
        else:
            await session.send('不支持的直播间地址', at_sender=True)
            return
    else:
        await help_(session)
        return
    ret = monitors[channel_type].add(channel_id, channel_name, group)
    monitors[channel_type].save()
    if ret == 0:
        await session.send(f'已存在：{channel_id} {channel_name}')
    elif ret == 3:
        await session.send(f'名称已修改：{channel_id} {channel_name}')
    else:
        await session.send(f'已添加：{channel_id} {ret.name if ret.name else ret.ch_name}')


async def del_(session: CommandSession, *argv: str):
    group = str(session.ctx['group_id'])
    channel_type = argv[1]
    channel_id = argv[2]
    ret = monitors[channel_type].remove(channel_id, group)
    monitors[channel_type].save()
    if ret:
        await session.send(f'已移除：{channel_id}')
    else:
        await session.send(f'未找到：{channel_id}')


async def list_(session: CommandSession, *argv: str):
    group = str(session.ctx['group_id'])
    sub = argv[1] if len(argv) >= 2 else ''
    final_msg = ''
    for monitor in monitors.values():
        msg = ''
        for ch in monitor.channel_list:
            if group in ch.targets:
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
    await session.send(final_msg.strip())


async def help_(session: CommandSession, *argv: str):
    msg = ''
    if not argv:
        argv = ['']
    if argv[0] == 'add':
        msg += 'monitor add <type> <cid> [name]\n'
        msg += 'monitor add <url> [name]\n'
        msg += '<url>:直播间地址\n'
        msg += '<type>:频道类型,备选值:bili,you,cc\n'
        msg += '<cid>:频道id,对于bilibili指直播间号\n'
        msg += '[name]:频道名,可省略\n'
    elif argv[0] == 'del':
        msg += 'monitor del <type> <cid>\n'
        msg += '<type>:频道类型\n'
        msg += '<cid>:频道id\n'
        msg += '注:可使用monitor list all查看频道id'
    elif argv[0] == 'list':
        msg += 'monitor list 查看频道及直播状态\n'
        msg += 'monitor list on 查看正在直播的频道\n'
        msg += 'monitor list all 查看所有频道及频道id\n'
    else:
        msg += 'monitor [command]\n'
        msg += 'command list: help, add, del, list\n'
        msg += '详细帮助（例）：monitor help add\n'
    await session.send(msg.strip())
