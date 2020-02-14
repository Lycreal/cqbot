import nonebot
from nonebot import on_command, CommandSession, MessageSegment, Message
from nonebot.permission import SUPERUSER

bot: nonebot.NoneBot = nonebot.get_bot()


class MsgFromText:
    @classmethod
    def msg_from_text(cls, text: str):
        text = text.strip()
        msg: Message = Message()
        for t in text.split():
            if not msg:
                msg.append(MessageSegment.text(' '))
            msg.append(cls.build(t))
        return msg

    @classmethod
    def build(cls, text: str):
        if text.startswith('@'):
            if text[1:].isdecimal():
                return MessageSegment.at(int(text[1:]))
        else:
            return MessageSegment.text(text)


@on_command('speak', aliases=('say', 'echo'), only_to_me=False, permission=SUPERUSER)
async def speak(session: CommandSession):
    group = session.get('group')
    word = session.get('word')
    msg = MsgFromText.msg_from_text(word)
    await bot.send_group_msg(group_id=group, message=msg)


@speak.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    try:
        group, word = stripped_arg.split(maxsplit=1)
        assert group.isdecimal()
        session.state['group'] = group
        session.state['word'] = word
    except (ValueError, AssertionError):
        session.state['group'] = str(session.ctx['group_id'])
        session.state['word'] = stripped_arg
    return
