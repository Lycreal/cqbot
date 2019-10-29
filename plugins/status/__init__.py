from datetime import datetime, timedelta
from nonebot import get_bot, on_command, CommandSession

bot = get_bot()
start_time = datetime.now()


@on_command('status', only_to_me=False)
async def _(session: CommandSession):
    now = datetime.now()
    uptime: timedelta = now - start_time
    msg = f'uptime: {uptime}'
    await session.send(msg)
