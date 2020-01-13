import asyncio
from nonebot import on_natural_language, NLPSession
from utils_bot.random_number import square_random


@on_natural_language('啾', only_to_me=True)
async def func(session: NLPSession):
    delay = square_random(2, 5)
    await asyncio.sleep(delay)
    await session.send('啾啾', at_sender=True)
