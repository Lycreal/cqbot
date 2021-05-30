import asyncio
from datetime import datetime, timedelta
from typing import Union

from nonebot import Bot
from nonebot import export
from nonebot import logger
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Message, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on
from nonebot.typing import T_State

from .config import plugin_config
from .model import NSFWChecker
from .moderatecontent import ModerateContentClient
from .rule import contain_image, is_defined
from .sightengine import SightEngineClient

if plugin_config.moderatecontent_apikey:
    NSFW_checker: NSFWChecker = ModerateContentClient(
        api_key=plugin_config.moderatecontent_apikey
    )
elif plugin_config.sightengine_api_user:
    NSFW_checker = SightEngineClient(
        api_user=plugin_config.sightengine_api_user,
        api_secret=plugin_config.sightengine_api_secret
    )
else:
    NSFW_checker = None

check_pic = on_command('检查', rule=is_defined(NSFW_checker), permission=SUPERUSER)
auto_recall = on("message_sent", rule=is_defined(NSFW_checker) & contain_image, permission=SUPERUSER)  # disable


@check_pic.handle()
async def check_pic_handler(bot: Bot, event: Event, state: T_State) -> None:
    if isinstance(event, MessageEvent) and event.reply:
        state['img_urls'] = [msg.data['url'] for msg in event.reply.message if msg.type == 'image']

        if state['img_urls']:
            img_url = state['img_urls'][0]
            level, description = await NSFW_checker.check_image(img_url)
            await bot.send(event, description)


@auto_recall.handle()
async def auto_recall_handler(bot: Bot, event: Event, state: T_State) -> None:
    img_url = state['img_urls'][0]
    time_sent = datetime.now()
    level, description = await NSFW_checker.check_image(img_url)
    logger.info(f'NSFW检查：{level}, {description}')
    if level == 1:  # adult
        time_to_sleep = time_sent + timedelta(seconds=10) - datetime.now()
        await asyncio.sleep(time_to_sleep.total_seconds())
        await bot.call_api('delete_msg', message_id=event.message_id)


@export()
async def check_and_recall(bot: Bot, message_id: int, image: Union[str, bytes, None] = None, delay: float = 10,
                           recall_by_default: bool = True) -> None:
    if NSFW_checker is None:
        return

    time_sent = datetime.now()

    if image is None:
        msg = await bot.get_msg(message_id=message_id)
        image_urls = [msg.data['url'] for msg in Message(msg['message']) if msg.type == 'image']
        image = image_urls[0]

    level = int(recall_by_default)
    try:
        level, description = await NSFW_checker.check_image(image)
        logger.info(f'NSFW检查：{level}, {description}')
    finally:
        if level == 1:
            time_to_sleep = time_sent + timedelta(seconds=delay) - datetime.now()
            await asyncio.sleep(time_to_sleep.total_seconds())
            await bot.call_api('delete_msg', message_id=message_id)
