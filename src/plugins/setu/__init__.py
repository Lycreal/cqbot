import asyncio
import random
import re
from base64 import b64encode

from nonebot import Bot, on_message, on_command
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import MessageEvent, Message, MessageSegment
from nonebot.plugin import require
from nonebot.typing import T_State

from .config import plugin_config
from .datasource import SetuResp
from .exceptions import TimeoutException
from .model import SetuData, SetuDatabase
from .utils import CoolDown, shuzi2number

setu_maximum = plugin_config.setu_maximum

cd = CoolDown(app='setu', td=20)

LAST_QUOTA: int = 300

NSFW_check = require('NSFW_check')
check_and_recall = NSFW_check.check_and_recall


async def setu_rule(bot: Bot, event: Event, state: T_State) -> bool:
    msg = event.get_plaintext()
    if match := re.match(r'(?:.*?([\d一二两三四五六七八九十]*)张|来点)?(.{0,10}?)的?色图$', msg):
        number: int = shuzi2number(match[1])
        number = min(number, setu_maximum, 10)
        keyword: str = match[2]

        state['number_of_setu'] = number
        state['keyword'] = keyword
        return True
    else:
        return False


setu = on_message(rule=setu_rule)
check_quota = on_command('色图配额')


@check_quota.handle()
async def checkQuota(bot: Bot, event: Event) -> None:
    resp = await SetuResp.get('色图配额')
    await bot.send(event, message=f'剩余配额：{resp.quota}\n恢复时间：{resp.time_to_recover.strftime("%m-%d %H:%M")}')


@setu.handle()
async def setuExecutor(bot: Bot, event: MessageEvent, state: T_State) -> None:
    """获取response"""
    global LAST_QUOTA
    keyword: str = state['keyword']

    member_id: int = event.sender.user_id

    if cd.check(member_id) is False:
        resp = SetuResp(code=-3, msg='技能冷却中')
    elif keyword == '' and len(SetuDatabase.load_from_file().__root__) >= 300 and LAST_QUOTA < 200:
        resp = SetuResp(code=-430, msg='空关键词')
    else:
        resp = await SetuResp.get(keyword)
        LAST_QUOTA = resp.quota

    state['setu_resp'] = resp


@setu.handle()
async def sendSetu(bot: Bot, event: MessageEvent, state: T_State) -> None:
    """发送data_array"""
    resp: SetuResp = state['setu_resp']

    if resp.code == 0:
        data_array = resp.data
    elif resp.code in [429, -430]:
        db = SetuDatabase.load_from_file()
        data_array = list(db.__root__)
    else:
        await bot.send(event, resp.msg)
        return

    number: int = state['number_of_setu']
    number = min(number, len(data_array))

    # 延时逐个启动任务

    num_exception = 0
    num_timeout = 0
    for i, data in enumerate(random.sample(data_array, k=number)):
        prefix = f'[{i + 1}/{number}]' if number > 1 else ''

        try:
            image_bytes = await data.get()
            file = f"base64://{b64encode(image_bytes).decode()}"
            ret = await bot.send(
                event,
                Message([MessageSegment.text(prefix), MessageSegment.image(file)]),
                at_sender=True
            )
            message_id = ret['data'].get('message_id')
            asyncio.create_task(check_and_recall(bot, message_id, image_bytes))

            cd.update(event.sender.user_id)
        except TimeoutException:
            num_timeout += 1
        except Exception:
            num_exception += 1

    # 报告结果
    if num_exception or num_timeout:
        msg_timeout = f'{num_timeout}个任务超时' if num_timeout else ''
        msg_exception = f'{num_exception}个任务异常' if num_exception else ''
        msg = msg_timeout or msg_exception
        if msg_timeout and msg_exception:
            msg += ', ' + msg_exception
        await bot.send(event, msg)
