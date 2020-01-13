import json
import urllib.request
import urllib.error
from . import BaseChannel


class BiliChannel(BaseChannel):
    def __init__(self, cid: str, name: str):
        super(BiliChannel, self).__init__(cid, name)
        # self.live_time: str = ''
        if not name:
            self.ch_name: str = self.get_bili_name(cid)

    def set_url(self):
        self.live_url = f'https://live.bilibili.com/{self.cid}'
        self.api_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={self.cid}'

    def resolve(self, html_s):
        json_d = json.loads(html_s)
        self.live_status = str(json_d['data']['live_status'])
        self.title = json_d['data']['title']
        # self.live_time = json_d['data']['live_time']
        if not self.name:
            try:
                self.ch_name: str = self.get_bili_name(self.cid)
            except (urllib.error.URLError, KeyError):
                self.name = self.ch_name

    # def notify(self) -> str:
    #     if self.live_status == '1':
    #         msg = f'[{self.live_time[11:16]}]{self.name}:{self.title} {self.live_url}'
    #     else:
    #         msg = f'{self.name}未开播'
    #     return msg

    @staticmethod
    def get_bili_name(cid: str):
        url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={cid}'
        with urllib.request.urlopen(url, timeout=10) as f:
            j = json.load(f)
        uid: int = j['data']['uid']

        url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
        with urllib.request.urlopen(url, timeout=10) as f:
            j = json.load(f)
        name = j['data']['name']
        return name
