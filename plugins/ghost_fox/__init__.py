# encoding: utf8

from utils_bot.msg_ops import send_to_groups
from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import Context_T, SUPERUSER
from typing import Dict, Union
from datetime import datetime, timedelta
import asyncio

__plugin_name__ = ''
__plugin_usage__ = r'''战言重现
'''

bot = get_bot()


class Ghost:
    def __init__(self, group):
        self.group = group
        self.record: Dict[float, str] = {}
        # self.next: Union[None, float] = None

    def income_msg(self, msg: str):
        if self.check(msg):
            time = datetime.now().timestamp() + 30
            # self.record.update({time: msg})
            # self.next = min(self.record.keys()) if self.record else None
            await asyncio.sleep(15)
            await bot.send_group_msg(group_id=self.group, message=str(msg).strip())

    def get_words(self):
        ret = {}
        now = datetime.now().timestamp()
        for time in sorted(self.record.keys()):
            if time <= now:
                ret.update(self.record.pop(time))
        return ret

    @staticmethod
    def check(msg: str) -> bool:
        watch = '爱❤❤️🧡💛💚💙💜🖤♥️💘💝💖💗💓💞💕❣❣️💟'
        if msg[0] in watch and msg[-1] in watch:
            return True
        elif '可爱' in msg and '喜欢' in msg:
            return True
        else:
            return False

    @staticmethod
    def take_time(elem: Dict[str, str]):
        return elem.keys()


ghosts: Dict[str, Ghost] = {}


@on_command('add_ghost', permission=SUPERUSER)
async def add_ghost(session: CommandSession):
    groups = session.current_arg_text.split()
    added = ''
    for group in groups:
        if group.isdecimal():
            ghosts.fromkeys(group, Ghost(group))
            added += group
    if added:
        await session.send(f'已添加：{added}')
