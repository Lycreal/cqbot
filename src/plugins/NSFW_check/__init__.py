import asyncio
import json
from datetime import datetime, timedelta
from typing import Union

from nonebot import Bot
from nonebot import export
from nonebot.adapters import Event
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on
from nonebot.typing import T_State

from .config import plugin_config
from .rule import contain_image
from .sightengine import SightEngineClient

NSFW_checker = SightEngineClient(
    api_user=plugin_config.sightengine_api_user,
    api_secret=plugin_config.sightengine_api_secret
)

check_pic = on_command('检查', permission=SUPERUSER)
auto_recall = on("message_sent", rule=contain_image, permission=SUPERUSER)  # disable


@check_pic.handle()
async def check_pic_handler(bot: Bot, event: Event, state: T_State) -> None:
    if isinstance(event, MessageEvent) and event.reply:
        state['img_urls'] = [msg.data['url'] for msg in event.reply.message if msg.type == 'image']

        if state['img_urls']:
            img_url = state['img_urls'][0]
            safe = json.dumps(await NSFW_checker.check_image(img_url))
            await bot.send(event, f'safe: {safe}')


@auto_recall.handle()
async def auto_recall_handler(bot: Bot, event: Event, state: T_State) -> None:
    img_url = state['img_urls'][0]
    time_sent = datetime.now()
    nudity = await NSFW_checker.check_image(img_url)
    if nudity['raw'] >= max(nudity['partial'], nudity['safe']):  # threshold
        time_to_sleep = time_sent + timedelta(seconds=10) - datetime.now()
        await asyncio.sleep(time_to_sleep.total_seconds())
        await bot.call_api('delete_msg', message_id=event.message_id)


@export()
async def check_and_recall(bot: Bot, message_id: int, image: Union[str, bytes]) -> None:
    time_sent = datetime.now()
    nudity = await NSFW_checker.check_image(image)

    if nudity['raw'] >= max(nudity['partial'], nudity['safe']):  # threshold
        time_to_sleep = time_sent + timedelta(seconds=10) - datetime.now()
        await asyncio.sleep(time_to_sleep.total_seconds())
        await bot.call_api('delete_msg', message_id=message_id)
