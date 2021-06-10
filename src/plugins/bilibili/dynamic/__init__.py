import re
from typing import List

from nonebot import Bot, on_command
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.log import logger
from nonebot.typing import T_State

from .datasource import getDynamicStatus
from .model import Target, Database


async def first_receive(bot: Bot, event: Event, state: T_State) -> None:
    msg: str = event.get_plaintext()
    uid_list: List[str] = re.compile(r'space.bilibili.com/(\d+)').findall(msg)
    if uid_list:
        state['uid_list'] = uid_list

    if isinstance(event, GroupMessageEvent):
        identifier = {'groups': {event.group_id}}
    else:
        identifier = {'users': {event.sender.user_id}}
    state['identifier'] = identifier


dynamic_monitor = on_command(('动态监控',), priority=10)
dynamic_monitor_add = on_command(('动态监控', '添加'), handlers=[first_receive], priority=2)
dynamic_monitor_del = on_command(('动态监控', '移除'), handlers=[first_receive], priority=3)
dynamic_monitor_show = on_command(('动态监控', '列表'), handlers=[first_receive], priority=4)


@dynamic_monitor.handle()
async def print_help(bot: Bot, event: Event, state: T_State) -> None:
    msg = '\n'.join([
        '使用说明:',
        '动态监控添加 <url1> ...',
        '动态监控移除 <url1> ...',
        '动态监控列表'
    ])
    await bot.send(event, message=msg)


@dynamic_monitor_add.got('uid_list', prompt='请输入动态地址', args_parser=first_receive)
async def add_handler(bot: Bot, event: Event, state: T_State) -> None:
    identifier = state['identifier']
    uid_list = state['uid_list']
    count: int = Database.add(*[Target(uid=uid, **identifier) for uid in uid_list])
    logger.info(f'「{identifier}」增加动态监控：{uid_list}')
    await bot.send(event, f'动态监控：新增{count}个频道')


@dynamic_monitor_del.got('uid_list', prompt='请输入动态地址', args_parser=first_receive)
async def del_handler(bot: Bot, event: Event, state: T_State) -> None:
    identifier = state['identifier']
    uid_list = state['uid_list']
    count: int = Database.remove(*[Target(uid=uid, **identifier) for uid in uid_list])
    logger.info(f'「{identifier}」移除动态监控：{uid_list}')
    await bot.send(event, f'动态监控：移除{count}个频道')


@dynamic_monitor_show.handle()
async def show_handler(bot: Bot, event: Event, state: T_State) -> None:
    identifier = state['identifier']
    names = Database.show(**identifier)
    msg = '动态监控列表：\n{}'.format('\n'.join(names)) if names else '动态监控列表为空'
    logger.info(f'「{identifier}」{msg}')
    await bot.send(event, msg)
