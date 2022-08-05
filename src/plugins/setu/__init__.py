import asyncio
import random
import re
import traceback
from base64 import b64encode
from typing import List, Optional

from nonebot import Bot, on_message, logger
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.plugin import require
from nonebot.typing import T_State
from numpy import bincount

from .config import plugin_config
from .datasource import SetuResp
from .exception import TimeoutException
from .model import SetuData, SetuDatabase
from .utils import CoolDown, shuzi2number, shuffle

setu_maximum = plugin_config.setu_maximum

cd = CoolDown(app='setu', td=20)

NSFW_check = require('NSFW_check')
check_and_recall = NSFW_check.check_and_recall


async def setu_rule(bot: Bot, event: Event, state: T_State) -> bool:
    msg = event.get_plaintext()
    if match := re.match(r'(?:.*?([\d一二两三四五六七八九十]*)张|来点)?(.{0,10}?)的?色图$', msg):
        number: int = shuzi2number(match[1])
        number = min(number, setu_maximum)
        keyword: str = match[2]

        state['number_of_setu'] = number
        state['keyword'] = keyword
        return True
    else:
        return False


setu = on_message(rule=setu_rule)


@setu.handle()
async def setuExecutor(bot: Bot, event: MessageEvent, state: T_State) -> None:
    """获取response"""
    keyword: str = state['keyword']

    member_id: int = event.sender.user_id

    if cd.check(member_id) is False:
        resp = SetuResp(code=-3, msg='技能冷却中')
    else:
        resp = await SetuResp.get(keyword)

    state['setu_resp'] = resp


@setu.handle()
async def sendSetu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    """发送data_array"""
    resp: SetuResp = state['setu_resp']

    data_array = resp.get_data()
    if not data_array:
        resp.code = -2  # blacklist keywords
        resp.msg = '没有符合条件的色图'

    if resp.code != 0:
        await bot.send(event, resp.msg)
        return

    number = min(state['number_of_setu'], len(data_array))

    async def send(setu_data_: SetuData) -> None:
        image_bytes = await setu_data_.get()
        if isinstance(event, GroupMessageEvent):
            image_bytes = shuffle(image_bytes)
        file = f"base64://{b64encode(image_bytes).decode()}"

        async with lock:
            logger.info(f'发送色图: {setu_data_.url}')
            ret = await bot.send(event, MessageSegment.image(file))
            cd.update(event.sender.user_id)

            if isinstance(event, GroupMessageEvent):
                message_id = ret['message_id']
                asyncio.create_task(check_and_recall(bot, message_id, image=image_bytes))

    # 延时逐个启动任务
    tasks: List[asyncio.Task[None]] = []
    lock = asyncio.Lock()
    for i, setu_data in enumerate(random.sample(data_array, k=number)):
        task = asyncio.create_task(send(setu_data))
        tasks.append(task)

    # 等待返回
    done, pending = await asyncio.wait(tasks, timeout=30)
    exceptions: List[Optional[BaseException]] = [task.exception() for task in done if task.exception()]
    num_exception, num_timeout = bincount([isinstance(exc, TimeoutException) for exc in exceptions], minlength=2).astype(object)
    num_timeout += len([t.cancel() for t in pending])

    for exc in exceptions:
        logger.error('\n'.join(traceback.format_exception(type(exc), exc, exc.__traceback__, limit=5)))

    # 报告结果
    if num_exception or num_timeout:
        msg_timeout = f'{num_timeout}个任务超时' if num_timeout else ''
        msg_exception = f'{num_exception}个任务异常' if num_exception else ''
        msg = msg_timeout or msg_exception
        if msg_timeout and msg_exception:
            msg += ', ' + msg_exception
        await bot.send(event, msg)
