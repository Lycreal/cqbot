import nonebot
from .run import do_search

__plugin_name__ = '查找B限'
__plugin_usage__ = r'''显示当前进行中的B限
命令：.B限 .b限 .b .B
'''


@nonebot.on_command('B限', aliases=('b限', 'b', 'B'), only_to_me=False)
async def _(session: nonebot.CommandSession):
    m: str = await do_search()
    if m:
        msg = '当前进行中的B限：\n' + m
    else:
        msg = '无进行中的B限'
    await session.send(msg)
