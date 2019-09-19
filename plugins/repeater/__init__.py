from nonebot import get_bot
# from nonebot.helpers import context_id
from nonebot.permission import Context_T
import time

__plugin_name__ = '复读机'
__plugin_usage__ = r'''feature: 复读
人类的本质
'''

# acquires global event monitor
bot = get_bot()


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

    async def simple_repeat(self, group_id: str, msg: str, wait_until: int = 3):
        # creates tracker for each group at beginning
        record = self.get_record(group_id)
        if msg != record.lastMsg:
            record.lastMsg, record.count = msg, 1
            return
        record.count += 1
        if record.count == wait_until:
            time.sleep(secs=1)
            await bot.send_group_msg(group_id=group_id, message=msg)
            record.count = -999


records = Records()


@bot.on_message('group')
async def _(ctx: Context_T):
    groupId = ctx['group_id']
    msg = ctx['raw_message']
    await records.simple_repeat(groupId, msg)
