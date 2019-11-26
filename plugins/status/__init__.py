from datetime import datetime, timedelta as ori_timedelta
from nonebot import get_bot, on_command, CommandSession


class timedelta(ori_timedelta):
    def __str__(self):
        mm, ss = divmod(self.seconds, 60)
        hh, mm = divmod(mm, 60)
        s = "%d:%02d:%02d" % (hh, mm, ss)
        if self.days:
            def plural(n):
                return n, abs(n) != 1 and "s" or ""

            s = ("%d day%s, " % plural(self.days)) + s
        return s


bot = get_bot()
start_time = datetime.now()


@on_command('status', only_to_me=False)
async def _(session: CommandSession):
    now = datetime.now()
    uptime: timedelta = now - start_time
    msg = f'uptime: {uptime}'
    await session.send(msg)
