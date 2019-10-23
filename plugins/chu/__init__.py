from nonebot import on_natural_language, NLPSession
import asyncio
import random


@on_natural_language('啾', only_to_me=True)
async def func(session: NLPSession):
    await asyncio.sleep(3 + random.random() * 5)
    await session.send('啾啾', at_sender=True)
