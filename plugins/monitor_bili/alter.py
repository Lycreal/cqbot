import urllib.request
from nonebot import on_command, CommandSession
import urllib.request
import json
import nonebot
from nonebot.permission import *
from datetime import datetime, timezone, timedelta
from plugins.monitor_bili.config import channel_list_bili, TIME_PRE
from config_private import GROUP_TST
from pathlib import Path

with urllib.request.urlopen('https://api.vtbs.moe/v1/info') as w:
    VTB_LIST = json.load(w)


def circle(n):
    x = 0
    while True:
        yield x
        x = x + 1 if x < n - 1 else 0


class Channel:
    live_status: int = 1
    live_time: str = '0000-00-00 00:00:00'  # 本次开播时间

    # last_live: str = '1970-01-02 00:00:00'  # 上次下播时间
    # last_check: str = '1970-01-02 00:00:00'  # 上次检测到直播时间

    def __init__(self, ch):
        self.mid = ch['mid']
        self.room_id: str = ch['roomid']
        self.name: str = ch['uname']
        self.live_url: str = f'https://api.vtbs.moe/v1/detail/{self.mid}'
        self.last_check = datetime.now(timezone(timedelta(hours=8)))

    def update(self):
        # 获取信息
        with urllib.request.urlopen(self.live_url) as w:
            json_s = w.read().decode('utf-8')
        json_d = json.loads(json_s)
        self.live_status = json_d['liveStatus']
        self.live_time = json_d['lastLive']['time']
        # 距离上次下播大于time_pre
        if self.live_status == 1 and datetime.now(timezone(timedelta(hours=8))) - self.last_check > TIME_PRE:
            ret = 1
        else:
            ret = 0
        # 开播状态
        if self.live_status == 1:
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间
            # self.last_live = self.last_check
        return ret

    def __str__(self):
        msg = f'Channel Name: {self.name}\n'
        self.update()
        msg += f'Live Status: {self.live_status}\n'
        msg += f'URL: https://live.bilibili.com/{self.room_id}'
        return msg


def load_list():
    if not Path.joinpath(Path(__file__).parent, 'monitor_list.py').is_file():
        monitor_list_alter = []
    else:
        with Path.joinpath(Path(__file__).parent, 'monitor_list.py').open(encoding='utf8') as f:
            monitor_list_alter = json.loads(f.read().replace("'", '"'))
    return monitor_list_alter


monitor_list_alter = load_list()
channels = [Channel(ch) for ch in monitor_list_alter]
v = circle(len(channels))

bot = nonebot.get_bot()
GROUPS = [GROUP_TST]


async def send_to_groups(msg: str):
    for groupId in GROUPS:
        await bot.send_group_msg(group_id=groupId, message=msg)


@nonebot.scheduler.scheduled_job('interval', seconds=5)
async def _():
    if channels:
        channel = channels[next(v)]
        if channel.update():
            if channel.live_status == 1:
                msg = f'{channel.name}开播了: '
                msg += f'https://live.bilibili.com/{channel.room_id}'
                await send_to_groups(msg)


@on_command('monitor_bili_add', only_to_me=False)
async def monitor_bili_add(session: CommandSession):
    global v
    global monitor_list_alter
    global channels
    monitor_list_alter = load_list()
    arg = session.get('monitor_bili_add')
    for vtb in VTB_LIST:
        if arg in (vtb['uname'], str(vtb['mid']), str(vtb['roomid'])):
            ch = {
                'uname': vtb['uname'],
                'mid': str(vtb['mid']),
                'roomid': str(vtb['roomid'])
            }
            if ch['roomid'] not in [x[0] for x in channel_list_bili] + [x['roomid'] for x in monitor_list_alter]:
                monitor_list_alter.append(ch)
                channels = [Channel(ch) for ch in monitor_list_alter]
                with Path.joinpath(Path(__file__).parent, 'monitor_list.py').open('w', encoding='utf8') as f:
                    f.write(str(monitor_list_alter))
                v = circle(len(channels))
                await session.send('已添加：%s' % {ch['uname']})
            else:
                await session.send('不可重复添加：%s' % {ch['uname']})
            return
    await session.send(f'未找到：{arg}')


@monitor_bili_add.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    session.state['monitor_bili_add'] = stripped_arg


@on_command('monitor_bili_alter_list', only_to_me=False)
async def monitor_bili_add(session: CommandSession):
    await session.send(str([x['uname'] for x in monitor_list_alter]))


@on_command('alter_add_group', permission=SUPERUSER)
async def alter_add_group(session: CommandSession):
    global GROUPS
    arg: str = session.get('alter_add_group')
    if arg and arg not in GROUPS:
        GROUPS.append(arg)
    await session.send(str(GROUPS))


@alter_add_group.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    session.state['alter_add_group'] = stripped_arg
