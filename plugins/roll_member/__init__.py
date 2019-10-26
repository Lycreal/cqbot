import random
from datetime import datetime, timedelta
from nonebot import get_bot, on_command, CommandSession

__plugin_name__ = '随机群员'
__plugin_usage__ = r'''feature: 随机群员
[关键词] rollmem rm
返回一名随机群员的id
'''


class RollMember:
    bot = get_bot()

    last_group = '0'
    last_check = datetime.fromtimestamp(100000)
    group_member_list = []

    @classmethod
    async def get(cls, group_id: str):
        now = datetime.now()
        if now - cls.last_check > timedelta(minutes=5) or group_id != cls.last_group:
            cls.group_member_list = await cls.bot.get_group_member_list(group_id=group_id)
            cls.last_check = now
            cls.last_group = group_id
        group_member_info = random.choice(cls.group_member_list)
        nickname = group_member_info['nickname']
        card = group_member_info['card']
        user_id = group_member_info['user_id']
        return f'{user_id}\n{card if card else nickname}'


RollMember()


@on_command('rollmember', aliases=('rm', 'rollmem'), only_to_me=False)
async def _(session: CommandSession):
    group_id = session.ctx['group_id']
    msg = await RollMember.get(group_id)
    await session.send(msg)
