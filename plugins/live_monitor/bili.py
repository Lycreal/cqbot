from plugins.live_monitor.general import BaseChannel
import json


class BiliChannel(BaseChannel):
    def __init__(self, cid: str, name: str):
        super(BiliChannel, self).__init__(cid, name)
        self.live_time = ''

    def get_url(self):
        self.live_url = f'https://live.bilibili.com/{self.cid}'
        self.api_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={self.cid}'

    def resolve(self, html_s):
        json_d = json.loads(html_s)
        self.live_status = str(json_d['data']['live_status'])
        self.title = json_d['data']['title']
        self.live_time = json_d['data']['live_time']

    def notify(self) -> str:
        if self.live_status == '1':
            msg = f'[{self.live_time[11:16]}]{self.name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg
