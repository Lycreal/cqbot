from plugins.live_monitor.general import BaseChannel
import json
import requests


class BiliChannel(BaseChannel):
    def __init__(self, cid: str, name: str):
        super(BiliChannel, self).__init__(cid, name)
        self.live_time: str = ''
        if not name:
            self.ch_name: str = self.get_bili_name(cid)

    def get_url(self):
        self.live_url = f'https://live.bilibili.com/{self.cid}'
        self.api_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={self.cid}'

    def resolve(self, html_s):
        json_d = json.loads(html_s)
        self.live_status = str(json_d['data']['live_status'])
        self.title = json_d['data']['title']
        self.live_time = json_d['data']['live_time']
        if not self.name:
            try:
                self.ch_name: str = self.get_bili_name(self.cid)
            except (requests.exceptions.ConnectionError, KeyError):
                self.name = self.ch_name

    def notify(self) -> str:
        if self.live_status == '1':
            msg = f'[{self.live_time[11:16]}]{self.name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg

    @staticmethod
    def get_bili_name(cid: str):
        j = json.loads(requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?id={cid}').text)
        if j['code'] != 0:
            return
        uid: int = j['data']['uid']
        j2 = json.loads(requests.get(f'https://api.kaaass.net/biliapi/user/space?id={uid}').text)
        name = j2['data']['card']['name']
        return name
