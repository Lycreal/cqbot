# encoding: utf8

import nonebot
from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import Context_T, SUPERUSER
from typing import Dict, Union
from datetime import datetime
import asyncio
from config_private import GROUP_BTR as G

__plugin_name__ = ''
__plugin_usage__ = r'''战言重现
'''

bot = get_bot()


class Ghost:
    def __init__(self, group):
        self.group: str = group
        self.record: Dict[float, str] = {}

    def income_msg(self, msg: str):
        if self.check(msg):
            time = datetime.now().timestamp()
            self.record.update({time: msg})

    def new_day(self):
        ret = self.record
        self.record = {}
        return ret

    @staticmethod
    def check(msg: str) -> bool:
        watch = '爱❤❤️🧡💛💚💙💜🖤♥️💘💝💖💗💓💞💕❣❣️💟🦊'
        if msg[0] in watch and msg[-1] in watch:
            return True
        elif '可爱' in msg and '喜欢' in msg:
            return True
        else:
            return False

    async def repeat(self, record):
        while record:
            now_last_day = datetime.now().timestamp() - 3600
            next_stamp = min(record.keys())
            delay = next_stamp - now_last_day
            await asyncio.sleep(delay)
            await bot.send_group_msg(group_id=self.group, message=record[next_stamp])
            record.pop(next_stamp)


ghost = Ghost(G)


# @on_command('set_ghost', only_to_me=False, permission=SUPERUSER)
# async def add_ghost(session: CommandSession):
#     global ghost
#     group = session.current_arg_text.strip()
#     if group.isdecimal():
#         ghost = Ghost(group)
#         await session.send(f'已添加：{group}')


@bot.on_message('group')
async def _(ctx: Context_T):
    groupId = str(ctx['group_id'])
    msg = ctx['raw_message']
    if groupId == ghost.group:
        ghost.income_msg(msg)


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    rec = ghost.new_day()
    await ghost.repeat(rec)

# @bot.on_message('group')
# async def _(ctx: Context_T):
#     groupId = str(ctx['group_id'])
#     msg = ctx['raw_message']
#     if Ghost.check(msg):
#         await asyncio.sleep(24 * 3600)
#         await bot.send_group_msg(group_id=groupId, message=msg)
