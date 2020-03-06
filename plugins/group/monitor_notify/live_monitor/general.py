from datetime import datetime, timezone, timedelta
from typing import List
import aiohttp
import abc
import difflib


class BaseChannel(abc.ABC):
    TIME_PRE = timedelta(minutes=5)

    def __init__(self, cid: str, name: str):
        self.api_url: str = ''
        self.live_url: str = ''
        self.live_status: str = '1'
        self.title: str = '<init>'
        self.ch_name: str = ''  # 频道名，自动获取
        self.cid: str = cid
        self.name: str = name  # 频道名，手动录入
        self.set_url()
        self.last_check: datetime = datetime.now(timezone(timedelta(hours=8))) - timedelta(days=30)
        self.last_title: str = '<init>'

        self.sendto: List[str] = []

    @abc.abstractmethod
    def set_url(self):
        # self.api_url: str = ''
        # self.live_url: str = ''
        raise NotImplementedError

    async def update(self) -> bool:
        last_status = self.live_status
        await self.__get_status()

        if self.live_status == '1':
            # 播报策略
            status_changed = last_status != self.live_status
            time_delta = datetime.now(timezone(timedelta(hours=8))) - self.last_check  # 距离上次检测到开播状态的时间
            title_changed = '<init>' != self.last_title and \
                            difflib.SequenceMatcher(None, self.last_title, self.title).quick_ratio() < 0.7  # 相似度较小

            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 记录开播时间
            self.last_title = self.title  # 记录开播标题

            if title_changed:  # 标题变更
                return True
            elif status_changed and time_delta >= timedelta(hours=1):  # 新开播，距上次开播1小时以上
                return True
            else:
                return False
        else:
            return False

    async def __get_status(self):
        async with aiohttp.request('GET', self.api_url, timeout=aiohttp.ClientTimeout(15)) as session:
            html_s = await session.text(encoding='utf8')

        self.resolve(html_s)

    @abc.abstractmethod
    def resolve(self, string: str):
        #     live_status: str
        #     title: str
        #     must be updated
        raise NotImplementedError

    def notify(self) -> str:
        if self.live_status == '1':
            msg = f'{self.name if self.name else self.ch_name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name if self.name else self.ch_name}未开播'
        return msg

    def __str__(self):
        msg = f'Name: {self.ch_name if self.ch_name else self.name}\n' \
              f'Title: {self.title}\n' \
              f'Live Status: {self.live_status}\n'
        return msg
