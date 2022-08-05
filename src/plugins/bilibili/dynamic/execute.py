from typing import TYPE_CHECKING

from nonebot import require, get_bots
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.log import logger

from .config import plugin_config
from .datasource import getDynamicStatus
from .model import Database

if TYPE_CHECKING:
    from nonebot_plugin_apscheduler import AsyncIOScheduler

scheduler: "AsyncIOScheduler" = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("interval", seconds=20, id="bili_dynamic")
async def execute() -> None:
    if bots := get_bots():
        bot = list(bots.values())[0]
    else:
        return

    db = Database.load()
    for target in db.__root__:
        if target.groups or target.users:
            try:
                resp = await getDynamicStatus(target.uid, debug=plugin_config.debug)
                if resp:
                    target.name = resp.name
                    footer = f"\n\n动态地址: https://t.bilibili.com/{resp.dynamic_id}"
                    logger.info(f'{target.name}动态更新：https://t.bilibili.com/{resp.dynamic_id}')

                    images = Message([MessageSegment.image(url) for url in resp.imgs])
                    message = Message(resp.msg) + images + footer

                    for group_id in target.groups:
                        await bot.send_group_msg(message=message, group_id=group_id)
                    for user_id in target.users:
                        await bot.send_private_msg(message=message, user_id=user_id)

            except Exception as e:
                import traceback
                logger.error(f'动态检查出错：{target.name} {e}')
                logger.error(traceback.format_exc())
                continue
    db.save_to_file()
