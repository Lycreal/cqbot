import random
from nonebot import on_command, CommandSession

__plugin_name__ = '骰子'
__plugin_usage__ = r'''feature: 骰子
[关键词] 骰子 roll rd
roll $number
返回不大于$number的正整数，默认值为6
'''

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('roll', aliases=('rd','Roll'), only_to_me=False)
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取数字上限（num_str），如果当前不存在，则询问用户
    num_str = session.get('roll')
    # 获取城市的天气预报
    roll_result = await get_result_of_roll(num_str)

    # 向用户发送天气预报
    await session.send(roll_result)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if not stripped_arg:
        stripped_arg = '6'
    session.state['roll'] = stripped_arg
    return


async def get_result_of_roll(num_str: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    try:
        num = int(num_str)
        assert num > 0
    except Exception as e:
        return '请输入正整数'
    result = random.randint(1, num)
    return str(result)
