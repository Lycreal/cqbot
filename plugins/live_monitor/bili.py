from plugins.live_monitor.general import BaseChannel
import json


class BiliChannel(BaseChannel):
    def get_url(self):
        self.live_url = f'https://live.bilibili.com/{self.cid}'
        self.api_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={self.cid}'

    def resolve(self, html_s):
        json_d = json.loads(html_s)
        self.live_status = str(json_d['data']['live_status'])
        self.title = json_d['data']['title']
