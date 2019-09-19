import urllib.request
from datetime import datetime, timezone, timedelta


class Channel:
    TIME_PRE = timedelta(minutes=10)
    last_check: datetime
    api_url: str
    live_url: str

    name: str = ''
    live_status: str = '0'
    title: str = ''

    def __init__(self):
        self.last_check = datetime.now(timezone(timedelta(hours=8)))

    def update(self) -> bool:
        self.get_status()
        if self.live_status == '1' and datetime.now(timezone(timedelta(hours=8))) - self.last_check > self.TIME_PRE:
            ret = True
        else:
            ret = False
        # 开播状态
        if self.live_status == '1':
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间
        return ret

    def get_status(self):
        with urllib.request.urlopen(self.api_url) as f:
            html_s = f.read().decode()
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
            msg = f'{self.name}开播了:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg
