from typing import Dict

from nonebot import Bot, logger
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.plugin import on, on_message
from nonebot.typing import T_State

from .model import PicSearcher
from .rule import full_match, contain_image

# ====================== 搜图 ======================
matcher_search_pic = on_message(rule=full_match('搜图'))


@matcher_search_pic.handle()
async def get_image_url(bot: Bot, event: Event, state: T_State) -> None:
    if img_urls := [msg.data['url'] for msg in event.get_message() if msg.type == 'image']:
        state['img_urls'] = img_urls
    # 从回复中搜图
    elif isinstance(event, MessageEvent) and event.reply:
        state['img_urls'] = [msg.data['url'] for msg in event.reply.message if msg.type == 'image']


@matcher_search_pic.got('img_urls', prompt='请发送图片')
async def search_pic(bot: Bot, event: Event, state: T_State) -> None:
    state['img_urls'] = [
        msg.data['url'] for msg in event.get_message() if msg.type == 'image'
    ]
    if img_urls := state.get('img_urls', [])[:1]:  # 限制为一张
        for img_url in img_urls:
            logger.info("搜图：%s" % repr(img_url))
            reply = await PicSearcher.do_search(img_url)
            await bot.send(event, reply)
    else:
        reply = '没有找到图片！操作已取消'
        await bot.send(event, reply)


# ====================== 搜上图 ======================
# 参考：https://github.com/synodriver/nonebot_plugin_picsearcher/blob/main/nonebot_plugin_picsearcher/__init__.py


matcher_record_pic = on_message(rule=contain_image)
matcher_record_pic_self = on("message_sent", rule=contain_image)
matcher_search_pic_last = on_message(rule=full_match('搜上图'))

pic_map: Dict[str, str] = {}  # 保存这个群的最近一张图 {"123456":http://xxx"}


@matcher_record_pic.handle()
@matcher_record_pic_self.handle()
async def record_pic(bot: Bot, event: Event, state: T_State) -> None:
    if isinstance(event, GroupMessageEvent):
        identifier = 'g' + str(event.group_id)
    elif isinstance(event, PrivateMessageEvent):
        identifier = 'p' + str(event.user_id)
    else:
        return
    pic_map[identifier] = state["img_urls"][0]


@matcher_search_pic_last.handle()
async def handle_previous(bot: Bot, event: Event) -> None:
    if isinstance(event, GroupMessageEvent):
        identifier = 'g' + str(event.group_id)
    elif isinstance(event, PrivateMessageEvent):
        identifier = 'p' + str(event.user_id)
    else:
        return

    if img_url := pic_map.get(identifier, None):
        reply = await PicSearcher.do_search(img_url)
        await bot.send(event, reply)
    else:
        reply = '未找到上一张图片'
        await bot.send(event, reply)
