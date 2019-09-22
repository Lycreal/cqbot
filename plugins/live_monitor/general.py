import requests
from requests.adapters import HTTPAdapter
from datetime import datetime, timezone, timedelta

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=0))
s.mount('https://', HTTPAdapter(max_retries=0))


class BaseChannel:
    TIME_PRE = timedelta(minutes=5)
    last_check: datetime
    api_url: str = ''
    live_url: str = ''
    cid: str = ''
    name: str = ''
    live_status: str = '1'
    title: str = ''
    ch_name: str = ''

    def __init__(self, cid: str, name: str):
        self.cid = cid
        self.name = name
        self.get_url()
        self.last_check = datetime.now(timezone(timedelta(hours=8))) - self.TIME_PRE

    def get_url(self):
        self.api_url = ''
        self.live_url = ''

    def update(self) -> bool:
        if self.live_status != '1':
            self.get_status()
            if self.live_status == '1':
                return True
        elif datetime.now(timezone(timedelta(hours=8))) - self.last_check >= self.TIME_PRE:
            self.get_status()
        return False

    def get_status(self):
        html_s = requests.get(self.api_url, timeout=10).text
        self.resolve(html_s)
        if self.live_status == '1':
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间

    def resolve(self, string: str):
        #     live_status: str
        #     title: str
        #     must be updated
        pass

    def notify(self) -> str:
        if self.live_status == '1':
            msg = f'{self.name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg

    def __str__(self):
        msg = f'Name: {self.ch_name if self.ch_name else self.name}\n' \
              f'Title: {self.title}\n' \
              f'Live Status: {self.live_status}\n'
        return msg
