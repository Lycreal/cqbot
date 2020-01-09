# encoding: utf8

from nonebot import on_command, CommandSession, get_bot, on_natural_language, NLPSession
from nonebot.permission import SUPERUSER, GROUP
from typing import Dict
from datetime import datetime
import asyncio

__plugin_name__ = ''
__plugin_usage__ = r'''战言重现
'''

bot = get_bot()


class Ghost:
    def __init__(self, group, timedelta: float = 0.):
        self.group: str = group if timedelta != 0 else '0'
        self.record: Dict[float, str] = {}
        self.timedelta = timedelta
        self.running = 0

    async def income_msg(self, msg: str):
        if self.check(msg):
            time = datetime.now().timestamp() + self.timedelta  # time to repeat
            self.record.update({time: msg})
            if not self.running:
                await self.run()

    @staticmethod
    def check(msg: str) -> bool:
        watch = '爱❤❤️🧡💛💚💙💜🖤♥️💘💝💖💗💓💞💕❣❣️💟🦊🍥⚓🏮'
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
            await asyncio.sleep(delay)
            await bot.send_group_msg(group_id=self.group, message=self.record[next_stamp])
            self.record.pop(next_stamp)
        self.running = 0


ghosts: Dict[str, Ghost] = {}


@on_command('set_ghost', only_to_me=False, permission=SUPERUSER)
async def add_ghost(session: CommandSession):
    argv = session.current_arg_text.split()
    group = argv[0]
    ts = float(argv[1]) if len(argv) >= 2 else 0.
    ghosts.update({group: Ghost(group, ts)})
    await session.send(f'已设置：{group} {ts}')


@on_natural_language(None, permission=GROUP, only_to_me=False)
async def _(session: NLPSession):
    if session.ctx['message_type'] != 'group':
        return
    group_id = str(session.ctx['group_id'])
    if group_id in ghosts.keys():
        ghost = ghosts[group_id]
        msg = session.ctx['raw_message']
        await ghost.income_msg(msg)
