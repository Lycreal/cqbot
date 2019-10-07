import nonebot
from nonebot import on_command, CommandSession
#
#
# def load_list():
#     if not Path.joinpath(Path(__file__).parent, 'monitor_list.py').is_file():
#         monitor_list_alter = []
#     else:
#         with Path.joinpath(Path(__file__).parent, 'monitor_list.py').open(encoding='utf8') as f:
#             monitor_list_alter = json.loads(f.read().replace("'", '"'))
#     return monitor_list_alter
#
#
# def save_list(monitor_list_alter: list):
#     with Path.joinpath(Path(__file__).parent, 'monitor_list.py').open('w', encoding='utf8') as f:
#         f.write(str(monitor_list_alter).replace('{', '\n{'))
#
#
# monitor_list_alter = load_list()
# channels = [monitor.init_channel(*ch) for ch in monitor_list_alter]
#
#
# @on_command('monitor_add', only_to_me=False)
# async def monitor_bili_add(session: CommandSession):
#     global v
#     global monitor_list_alter
#     global channels
#     monitor_list_alter = load_list()
#     arg = session.get('monitor_bili_add')
#     for vtb in VTB_LIST:
#         if arg in (vtb['uname'], str(vtb['mid']), str(vtb['roomid'])):
#             ch = {
#                 'uname': vtb['uname'],
#                 'mid': str(vtb['mid']),
#                 'roomid': str(vtb['roomid'])
#             }
#             if ch['roomid'] not in [x[0] for x in channel_list_bili] + [x['roomid'] for x in monitor_list_alter]:
#                 monitor_list_alter.append(ch)
#                 channels = [Channel(ch) for ch in monitor_list_alter]
#                 save_list(monitor_list_alter)
#                 v = circle(len(channels))
#                 await session.send('已添加：%s' % {ch['uname']})
#             else:
#                 await session.send('不可重复添加：%s' % {ch['uname']})
#             return
#     await session.send(f'未找到：{arg}')
#
#
# @monitor_bili_add.args_parser
# async def _(session: CommandSession):
#     stripped_arg = session.current_arg_text.strip()
#     session.state['monitor_bili_add'] = stripped_arg
#
#
# @on_command('monitor_bili_alter_list', only_to_me=False)
# async def monitor_bili_add(session: CommandSession):
#     await session.send(str([x['uname'] for x in monitor_list_alter]))
#
#
# @on_command('alter_add_group', permission=SUPERUSER)
# async def alter_add_group(session: CommandSession):
#     global GROUPS
#     arg: str = session.get('alter_add_group')
#     if arg and arg not in GROUPS:
#         GROUPS.append(arg)
#     await session.send(str(GROUPS))
#
#
# @alter_add_group.args_parser
# async def _(session: CommandSession):
#     stripped_arg = session.current_arg_text.strip()
#     session.state['alter_add_group'] = stripped_arg


# @nonebot.on_command('monitor_bili_status', only_to_me=False)
# async def monitor_bili_status(session: nonebot.CommandSession):
#     await session.send(str(monitor_bili).strip())
#
# @nonebot.on_command('monitor_cc_status', only_to_me=False)
# async def monitor_cc_status(session: nonebot.CommandSession):
#     await session.send(str(monitor).strip())
#
# @nonebot.on_command('monitor_you_status', only_to_me=False)
# async def monitor_you_status(session: nonebot.CommandSession):
#     await session.send(str(monitor_you).strip())
