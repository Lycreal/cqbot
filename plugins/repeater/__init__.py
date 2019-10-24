from nonebot import on_natural_language, NLPSession
from nonebot.permission import GROUP
import random
import asyncio

__plugin_name__ = '复读机'
__plugin_usage__ = r'''feature: 复读
人类的本质
'''


class Record:
    def __init__(self, lastMsg: str, count=1):
        self.lastMsg = lastMsg
        self.count = count


class Records(dict):
    def get_record(self, group_id: str) -> Record:
        """creates tracker for each group at beginning"""
        record = self.get(group_id)
        if record is None:
            record = Record('', 0)
            self[group_id] = record
        return record

    def simple_repeat(self, group_id: str, msg: str, wait_until: int = 3):
        # creates tracker for each group at beginning
        record = self.get_record(group_id)
        if msg != record.lastMsg:
            record.lastMsg, record.count = msg, 1
            return
        record.count += 1
        if record.count == wait_until:
            return msg


records = Records()


# @bot.on_message('group')
# async def _(ctx: Context_T):
#     groupId = ctx['group_id']
#     msg = ctx['raw_message']
#     word = records.simple_repeat(groupId, msg)
#     if word:
#         await asyncio.sleep(3)
#         await bot.send_group_msg(group_id=groupId, message=word)


@on_natural_language(None, permission=GROUP, only_to_me=False)
async def _(session: NLPSession):
    groupId = session.ctx['group_id']
    msg = session.ctx['raw_message']
    word = records.simple_repeat(groupId, msg)
    if word:
        await asyncio.sleep(2 + 3 * random.random() ** 2)
        await session.send(word)
