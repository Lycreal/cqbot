import requests
from datetime import datetime, timezone, timedelta


class Channel:
    TIME_PRE = timedelta(minutes=10)
    last_check: datetime
    api_url: str = ''
    live_url: str = ''
    id: str = ''
    name: str = ''
    live_status: str = '1'
    title: str = ''

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.get_url()
        self.last_check = datetime.now(timezone(timedelta(hours=8))) - self.TIME_PRE
        return

    def get_url(self):
        self.api_url = ''
        self.live_url = ''

    def update(self) -> bool:
        ret = False
        if self.live_status != '1':
            self.get_status()
            if self.live_status == '1':
                ret = True
        elif datetime.now(timezone(timedelta(hours=8))) - self.last_check >= self.TIME_PRE:
            self.get_status()
        # 开播状态
        if self.live_status == '1':
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间
        return ret

    def get_status(self):
        html_s = requests.get(self.api_url).text
        self.resolve(html_s)

    def resolve(self, string: str):
        #     live_status: str
        #     title: str
        #     must be updated
        pass

    def __str__(self):
        msg = f'Name: {self.name}\n' \
              f'Title: {self.title}\n' \
              f'Live Status: {self.live_status}\n'
        return msg

    def notify(self):
        if self.live_status == '1':
            msg = f'{self.name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg
