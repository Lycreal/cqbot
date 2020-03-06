import random
import math
from datetime import datetime, timezone, timedelta

from nonebot import on_command, CommandSession

# from nonebot.permission import *

__plugin_name__ = '今日运气'
__plugin_usage__ = f'''feature: 看看今天的运气~
[关键词] 今日运气 今日人品 jrrp
不为结果负责。
'''


class TestLuck:

    @staticmethod
    def return_luck_by_num(num: float) -> str:
        """
        :param num:0-1的数字
        :return:0-100的数字
        """
        luck = math.sqrt(num)
        return str(round(luck * 100))

    @classmethod
    def generate_luck_result(cls, sender_id: int) -> str:
        senderId: int = sender_id
        timeStamp: int = int(
            datetime.now(timezone(timedelta(hours=8))).strftime('%m%d%Y')
        )
        seed: int = (senderId * 7) ^ (timeStamp * 333)
        random.seed(seed)
        res: float = random.random()
        random.seed()
        return cls.return_luck_by_num(res)


@on_command('今日运气', aliases=('今日运气', '今日人品', 'jrrp'), only_to_me=False)
async def my_luck_today(session: CommandSession):
    senderId: int = int(session.ctx['user_id'])
    await session.send(TestLuck.generate_luck_result(senderId), at_sender=True)
