import random
from nonebot import get_bot, on_command, CommandSession

__plugin_name__ = '随机群员'
__plugin_usage__ = r'''feature: 随机群员
[关键词] rollmem rm
返回一名随机群员的id
'''

bot = get_bot()


@on_command('rollmember', aliases=('rm', 'rollmem'), only_to_me=False)
async def weather(session: CommandSession):
    group_id = session.ctx['group_id']
    group_member_list = await bot.get_group_member_list(group_id=group_id)
    group_member_info = random.choice(group_member_list)
    nickname = group_member_info['nickname']
    card = group_member_info['card']
    user_id = group_member_info['user_id']
    await session.send(f'{user_id}\n{card if card else nickname}')
