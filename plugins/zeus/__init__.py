# 出处 https://bbs.nga.cn/read.php?tid=17610345

import random
from nonebot import CommandSession, on_command

__plugin_name__ = '宙斯模拟器'
__plugin_usage__ = r'''feature: 宙斯模拟器
[关键词] zeus 宙斯
zeus <number>
进化次数为<number>的宙斯模拟器，默认值为6
'''


class Zeus:
    def __init__(self):
        self.txt = ''
        self.atk_bonus = 0
        self.defense_bonus = 0
        self.hp_restore = 0
        self.blind = False
        self.bane = False
        self.storm = False
        self.guard = False

    def activate_once(self):
        r = random.randint(1, 5)
        if r == 1:
            self.hp_restore += 5
            self.txt += "你的主战者回复了5点体力！\n"
        elif r == 2:
            self.atk_bonus += 3
            self.blind = True
            self.txt += "至高神·宙斯获得了+3/+0！ 至高神·宙斯可以无视守护进行攻击！\n"
        elif r == 3:
            self.storm = True
            self.atk_bonus += 2
            self.defense_bonus += 1
            self.txt += "至高神·宙斯获得了+2/+1！ 至高神·宙斯获得了疾驰！\n"
        elif r == 4:
            self.bane = True
            self.atk_bonus += 1
            self.defense_bonus += 2
            self.txt += "至高神·宙斯获得了+1/+2！ 至高神·宙斯获得了必杀！\n"
        elif r == 5:
            self.guard = True
            self.defense_bonus += 3
            self.txt += "至高神·宙斯获得了+0/+3！ 至高神·宙斯获得了守护！\n"

    def activate(self, evolve_count):
        self.txt += "宙斯的入场曲发动了！\n"
        for i in range(evolve_count):
            self.activate_once()

    def __str__(self):
        self.txt += '\n'
        self.txt += "啊，这强大的力量，即使是邪龙林德沃姆也无法企及！\n" if self.storm and self.atk_bonus >= 6 else ""
        self.txt += "啊，这可靠的身躯，能超越万雷之君的只有他自己！\n" if self.guard and self.defense_bonus >= 6 else ""
        self.txt += "啊，神王的仁慈，轻而易举便超越了美食天使的全力！\n" if self.hp_restore >= 15 else ""
        self.txt += "神王的召唤仪式好像出现了什么差错......\n" if self.storm is False and self.guard is False else ""

        self.txt += "庆贺吧！他是全知全能，位于诸神顶点的众神之父、万雷之主————至高神·宙斯！\n此刻，他携带着崭新的进化之力降临，" \
                    "让世间重现神之荣光！\n" if self.blind and self.bane and self.storm and self.guard else ""

        self.txt += "至高神·宙斯使你的主战者回复了%d点血量!\n" % self.hp_restore if self.hp_restore != 0 else ""
        self.txt += "至高神·宙斯具有了异能 " if self.blind or self.bane or self.storm or self.guard else ""
        self.txt += "无视守护 " if self.blind else ""
        self.txt += "必杀 " if self.bane else ""
        self.txt += "疾驰 " if self.storm else ""
        self.txt += "守护 " if self.guard else ""
        self.txt += "\n"
        self.txt += "至高神·宙斯现身为"
        self.txt += "%d/%d!" % (self.atk_bonus + 5, self.defense_bonus + 5)
        return self.txt


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('zeus', aliases=('Zeus', '宙斯'))
async def zeus(session: CommandSession):
    # 从会话状态（session.state）中获取数字上限（num_str），如果当前不存在，则询问用户
    num_str = session.get('times')
    # 获取城市的天气预报
    roll_result = await get_result_of_roll(num_str)
    # 向用户发送天气预报
    await session.send(roll_result)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@zeus.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if not stripped_arg:
        stripped_arg = '6'
    session.state['times'] = stripped_arg
    return


async def get_result_of_roll(num_str: str) -> str:
    try:
        num = int(num_str)
        assert num > 0
    except ValueError or AssertionError:
        return '请输入正整数'
    evolve = num
    zenx = Zeus()
    zenx.activate(evolve)
    result = '====至高神模拟器====\n本局随从进化次数: %s\n' % num
    result += str(zenx)
    return result
