from nonebot import NoticeSession, RequestSession, on_notice, on_request, get_bot

from utils_bot.msg_ops import send_to_superusers

__plugin_usage__ = r'''feature: 处理群邀请
'''


# accepts group invites only from superusers, instantly
@on_request('group.invite')
async def _(session: RequestSession):
    sender = session.ctx['user_id']
    await session.approve()
    await send_to_superusers(
        f'接受了群{session.ctx["group_id"]}的邀请。(发起人：{sender})')
    # if sender in SUPERUSERS:
    #     await session.approve()
    #     await send_to_superusers(
    #         f'接受了群{session.ctx["group_id"]}的邀请。(发起人：{sender})')
    # else:
    #     await session.reject()


@on_request('friend')
async def _(session: RequestSession):
    await send_to_superusers(f'{session.ctx["user_id"]}请求添加好友，附加消息：{session.ctx["comment"]}')


# notify superusers when bot joins a group
@on_notice('group_increase')
async def _(session: NoticeSession):
    await send_to_superusers(f'{session.ctx["user_id"]}加入了群{session.ctx["group_id"]}。')


# notify superusers when bot gets kicked from a group
@on_notice('group_decrease')
async def _(session: NoticeSession):
    if session.ctx["user_id"] != session.ctx["operator_id"]:
        await send_to_superusers(
            f'{session.ctx["user_id"]}被{session.ctx["operator_id"]}踢出了群{session.ctx["group_id"]}。')
    else:
        await send_to_superusers(
            f'{session.ctx["user_id"]}离开了群{session.ctx["group_id"]}。')
        await get_bot().send_group_msg(group_id=session.ctx["group_id"],
                                       message=f'{session.ctx["user_id"]}离开了本群')


# notify superusers when bot is set admin
@on_notice('group_admin.set')
async def _(session: NoticeSession):
    await send_to_superusers(
        f'{session.ctx["user_id"]}被群{session.ctx["group_id"]}设置为管理员。')


# notify superusers when bot is unset admin
@on_notice('group_admin.unset')
async def _(session: NoticeSession):
    await send_to_superusers(
        f'{session.ctx["user_id"]}被群{session.ctx["group_id"]}取消管理员。')
