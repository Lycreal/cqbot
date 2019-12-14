import pickle
import pathlib
from pydantic import BaseModel, ValidationError
from typing import Dict, List, Any, Type
from datetime import datetime
import nonebot
from nonebot import on_command, CommandSession, on_natural_language, NLPSession
from bot import root_path


class Statistics(BaseModel):
    loaded = False
    data_count: Dict[int, Dict[int, int]] = {}  # 计数用字典
    data_time: Dict[int, List[datetime]] = {}  # 计时用字典
    data_name: Dict[int, Dict[int, str]] = {}  # 保存名字的字典
    last_day_msg_count: Dict[int, str] = {}  # 昨日计数
    last_day_msg_time: Dict[int, str] = {}  # 昨日计时

    last_save_time = None
    save_file = pathlib.Path(root_path).joinpath('data').joinpath('statistics.dat')

    @classmethod
    def load(cls):
        try:
            if cls.save_file.exists():
                with cls.save_file.open('rb') as f:
                    save_data = pickle.load(f)
                cls.data_count, cls.data_time, cls.data_name, cls.last_day_msg_count, cls.last_day_msg_time = save_data
            else:
                cls.save()
        except ValidationError:
            cls.save()
        cls.loaded = True

    @classmethod
    def save(cls):
        save_data = cls.data_count, cls.data_time, cls.data_name, cls.last_day_msg_count, cls.last_day_msg_time
        with cls.save_file.open('wb') as f:
            pickle.dump(save_data, f)

    @classmethod
    def incoming_msg(cls, group_id: int, user_id: int, name: str):
        if not cls.loaded:
            cls.load()
        cls.init(group_id, user_id, name)
        cls.data_count[group_id][user_id] += 1
        cls.data_time[group_id].append(datetime.now())
        cls.save()

    @classmethod
    def init(cls, group_id: int, user_id: int, name: str):
        # 初始化group_id和user_id结构
        if group_id not in cls.data_time.keys():
            cls.data_time.update({group_id: []})

        if group_id not in cls.data_count.keys():
            cls.data_count.update({group_id: {}})
        if user_id not in cls.data_count[group_id].keys() and user_id:
            cls.data_count[group_id].update({user_id: 0})

        if group_id not in cls.data_name.keys():
            cls.data_name.update({group_id: {}})
        cls.data_name[group_id].update({user_id: name})

    @classmethod
    def clear(cls):
        for group_id in cls.data_count.keys():
            cls.last_day_msg_count.update({group_id: cls.top_talker(group_id)})
        for group_id in cls.data_time.keys():
            cls.last_day_msg_time.update({group_id: cls.time_result(group_id)})
        cls.data_count = {}
        cls.data_time = {}

    @classmethod
    def top_talker(cls, group_id: int, number=5):  # <20
        listed = cls.sort_dict(cls.data_count[group_id])
        msg = f'今日发言Top{number}:'
        for i in range(number if len(listed) > number else len(listed)):
            user_id = listed[i][0]
            count = listed[i][1]
            msg += f'\n{cls.data_name[group_id][user_id]}:{count}'
        return msg

    @classmethod
    def time_result(cls, group_id: int):
        result = [time.hour - 4 if time.hour >= 4 else time.hour + 24 - 4 for time in cls.data_time[group_id]]
        a = [0] * 12
        for i in range(12):
            a[i] += result.count(0 + 2 * i)
            a[i] += result.count(1 + 2 * i)
        char = '█'
        max_display = 12 if max(a) < 1000 else 11

        msg = '今日发言时段（4点起，每2小时）：'
        for i in range(12):
            msg += '\n' + round(max_display * a[i] / max(a)) * char + str(a[i])
        return msg

    @staticmethod
    def sort_dict(dict_words):
        """
        字典排序
        :param dict_words:
        :return:
        """
        keys = dict_words.keys()
        values = dict_words.values()

        list_one = [(key, val) for key, val in zip(keys, values)]
        list_sort = sorted(list_one, key=lambda x: x[1], reverse=True)

        return list_sort


@on_natural_language('', only_to_me=False)
async def record(session: NLPSession):
    group_id: int = session.ctx['group_id']
    sender: Dict[str, Any] = session.ctx['sender']

    user_id: int = sender['user_id']
    nickname: str = sender['nickname']
    card: str = sender['card']

    name = card if card else nickname
    Statistics.incoming_msg(group_id, user_id, name)


@on_command('statistics', aliases=('stat', '统计', 'tj'), only_to_me=False)
async def _(session: CommandSession):
    group_id: int = session.ctx['group_id']
    arg = session.current_arg_text.strip()
    if arg.isdecimal():
        msg = Statistics.top_talker(group_id, int(arg))
    else:
        msg = Statistics.top_talker(group_id)
    await session.send(msg)


@on_command('stat2', only_to_me=False)
async def _(session: CommandSession):
    group_id: int = session.ctx['group_id']
    msg = Statistics.time_result(group_id)
    await session.send(msg)


@on_command('stat3', only_to_me=False)
async def _(session: CommandSession):
    group_id: int = session.ctx['group_id']
    msg = Statistics.last_day_msg_count[group_id].replace('今日', '昨日')
    await session.send(msg)


@on_command('stat4', only_to_me=False)
async def _(session: CommandSession):
    group_id: int = session.ctx['group_id']
    msg = Statistics.last_day_msg_time[group_id].replace('今日', '昨日')
    await session.send(msg)


@nonebot.scheduler.scheduled_job('cron', hour='4')
async def _():
    Statistics.clear()
