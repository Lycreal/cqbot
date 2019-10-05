import nonebot
from nonebot import on_command, CommandSession
from nonebot.permission import SUPERUSER

bot: nonebot.NoneBot = nonebot.get_bot()


@on_command('speak', aliases=('say', 'echo'), only_to_me=False, permission=SUPERUSER)
async def speak(session: CommandSession):
    group = session.get('group')
    word = session.get('word')
    await bot.send_group_msg(group_id=group, message=word)


@speak.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    try:
        group, word = stripped_arg.split(maxsplit=1)
        assert group.isdecimal()
        session.state['group'] = group
        session.state['word'] = word
    except ValueError or AssertionError:
        session.state['group'] = str(session.ctx['group_id'])
        session.state['word'] = stripped_arg
    return
