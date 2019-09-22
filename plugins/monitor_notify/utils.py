# from datetime import timedelta
import nonebot


# TIME_PRE = timedelta(minutes=5)

def circle(n):
    x = 0
    while True:
        yield x
        x = x + 1 if x < n - 1 else 0


bot = nonebot.get_bot()


async def send_to_groups(GROUPS: list, msg: str):
    for groupId in GROUPS:
        await bot.send_group_msg(group_id=groupId, message=msg)


channel_list_bili = [
    ('12235923', '神楽めあ'),
    ('21304638', '神楽七奈'),

    ('8899503', '时乃空'),
    ('4664126', '萝卜子'),
    ('21144047', '樱巫女'),
    ('11588230', '白上吹雪'),
    ('13946381', '夏色祭'),
    ('14275133', '赤井心'),
    ('21219990', '亚绮-罗森'),
    ('21131813', '夜空梅露'),

    ('21107534', '癒月巧可'),
    ('21129632', '大空昴'),
    ('21132965', '紫咲诗音'),
    ('21130785', '百鬼绫目'),
    ('14917277', '湊-阿库娅'),

    ('21133979', '大神澪'),
    ('21420932', '猫又小粥'),
    ('21421141', '戌神沁音'),

    ('21584153', '宝钟玛琳'),
    ('21583736', '白银诺艾尔'),
    ('21572617', '不知火芙蕾雅'),
    ('21545232', '润羽露西娅'),
    ('21560356', '兔田佩克拉'),

    ('190577', '星街彗星'),
    ('21267062', 'AZKi')
]

channel_list_you = [
    ('UCWCc8tO-uUl_7SJXIKJACMw', '神楽めあ'),
    ('UC1opHUrw8rvnsadT-iGp7Cg', '湊あくあ'),
    ('UCdn5BQ06XqgXoAxIhbqw5Rg', '白上フブキ')
]

channel_list_cc = [
    ('361433', 'Mr.Quin'),
]
