from asyncio import sleep

from nonebot import Bot
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
auto_recall = on("message_sent", rule=contain_image)


@check_pic.handle()
async def _(bot: Bot, event: Event, state: T_State) -> None:
    if isinstance(event, MessageEvent) and event.reply:
        state['img_urls'] = [msg.data['url'] for msg in event.reply.message if msg.type == 'image']

        if state['img_urls']:
            img_url = state['img_urls'][0]
            safe = await NSFW_checker.check_image(img_url)
            await bot.send(event, f'safe: {safe}')


@auto_recall.handle()
async def _(bot: Bot, event: Event, state: T_State) -> None:
    img_url = state['img_urls'][0]
    safe = await NSFW_checker.check_image(img_url)
    if safe < 0.5:  # threshold
        await sleep(10)
        await bot.call_api('delete_msg', message_id=event.message_id)
