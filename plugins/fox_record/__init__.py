from nonebot import on_command, CommandSession, get_bot
from nonebot.permission import Context_T
from config_private import GROUP_BTR

__plugin_name__ = ''
__plugin_usage__ = r'''战言统计
'''

bot = get_bot()

record_image = {}
record_fox = {}
record_fox_emoji = {}


@bot.on_message('group')
async def _(ctx: Context_T):
    if ctx['group_id'] == GROUP_BTR and ctx['sender']['role'] == 'owner':
        if ctx

        msg = ctx['raw_message']
        await records.simple_repeat(groupId, msg)
