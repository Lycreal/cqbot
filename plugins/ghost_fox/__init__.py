# encoding: utf8

from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import Context_T, SUPERUSER
from typing import Dict, List
from datetime import datetime
import asyncio

__plugin_name__ = ''
__plugin_usage__ = r'''战言重现
'''

bot = get_bot()


class Ghost:
    def __init__(self, group, timedelta: float = 0.):
        self.group: str = group
        self.record: Dict[float, str] = {}
        self.timedelta = timedelta if timedelta != 0. else 3600.
        self.running = 0

    async def income_msg(self, msg: str):
        if self.check(msg):
            time = datetime.now().timestamp() + self.timedelta  # time to repeat
            self.record.update({time: msg})
            if not self.running:
                await self.run()

    @staticmethod
    def check(msg: str) -> bool:
        watch = '爱❤❤️🧡💛💚💙💜🖤♥️💘💝💖💗💓💞💕❣❣️💟🦊'
        if msg[0] in watch and msg[-1] in watch:
            return True
        elif '可爱' in msg and '喜欢' in msg:
            return True
        else:
            return False

    async def run(self):
        self.running = 1
        while self.record:
            now = datetime.now().timestamp()
            next_stamp = min(self.record.keys())
            delay = next_stamp - now
            # if delay > 5 * 60:
            await asyncio.sleep(delay)
            await bot.send_group_msg(group_id=self.group, message=self.record[next_stamp])
            self.record.pop(next_stamp)
            # else:
            #     msg = self.record.pop(next_stamp)
            #     self.record.update({next_stamp + self.timedelta: msg})
        self.running = 0


ghosts: List[Ghost] = []


@on_command('set_ghost', only_to_me=False, permission=SUPERUSER)
async def add_ghost(session: CommandSession):
    argv = session.current_arg_text.split()
    group = argv[0]
    ts = float(argv[1]) if len(argv) >= 2 else 0.
    ghosts.append(Ghost(group, ts))
    await session.send(f'已添加：{group} {ts}')


@bot.on_message('group')
async def _(ctx: Context_T):
    group_id = str(ctx['group_id'])
    msg = ctx['raw_message']
    for ghost in ghosts:
        if group_id == ghost.group:
            await ghost.income_msg(msg)
