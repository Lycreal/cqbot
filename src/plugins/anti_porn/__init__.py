from nonebot import Bot
from nonebot.plugin import on_command
from nonebot.adapters import Event
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER

from .model import AccessToken, AntiPorn
from .config import plugin_config

anti_porn = AntiPorn(access_token=AccessToken(
    api_key=plugin_config.baidu_api_key,
    secret_key=plugin_config.baidu_secret_key,
    access_token=plugin_config.baidu_access_token
))

check_pic = on_command('检查', permission=SUPERUSER)


@check_pic.handle()
async def _(bot: Bot, event: Event, state: T_State) -> None:
    if isinstance(event, MessageEvent) and event.reply:
        state['img_urls'] = [msg.data['url'] for msg in event.reply.message if msg.type == 'image']

        if state['img_urls']:
            img_url = state['img_urls'][0]
            reply = await anti_porn.check_image(img_url)
            await bot.send(event, reply)
