import asyncio
import random
import re
from base64 import b64encode

from nonebot import Bot, on_message, logger
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.plugin import require
from nonebot.typing import T_State

from .config import plugin_config
from .datasource import SetuResp
from .exceptions import TimeoutException
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

    if resp.code != 0:
        await bot.send(event, resp.msg)
        return

    data_array = resp.data
    number = min(state['number_of_setu'], len(data_array))

    # 延时逐个启动任务
    num_exception = 0
    num_timeout = 0
    for i, setu_data in enumerate(random.sample(data_array, k=number)):
        try:
            image_bytes = await setu_data.get()

            if isinstance(event, GroupMessageEvent):
                image_bytes = shuffle(image_bytes)

            file = f"base64://{b64encode(image_bytes).decode()}"
            logger.info(f'发送色图: {setu_data.url}')
            ret = await bot.send(event, MessageSegment.image(file))

            if isinstance(event, GroupMessageEvent):
                message_id = ret['message_id']
                asyncio.create_task(check_and_recall(bot, message_id, image=image_bytes))

            cd.update(event.sender.user_id)
        except TimeoutException as e:
            import traceback
            logger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))
            num_timeout += 1
        except Exception as e:
            import traceback
            logger.error('\n'.join(traceback.format_exception(type(e), e, e.__traceback__)))
            num_exception += 1

    # 报告结果
    if num_exception or num_timeout:
        msg_timeout = f'{num_timeout}个任务超时' if num_timeout else ''
        msg_exception = f'{num_exception}个任务异常' if num_exception else ''
        msg = msg_timeout or msg_exception
        if msg_timeout and msg_exception:
            msg += ', ' + msg_exception
        await bot.send(event, msg)
