import re
from plugins.monitor_notify.live_monitor import BaseChannel


class NetEaseChannel(BaseChannel):
    def get_url(self):
        self.live_url = f'https://cc.163.com/{self.cid}/'
        self.api_url = self.live_url

    def resolve(self, html_s):
        room_info = re.search(r'<script type="text/javascript">\s+var roomInfo(.*?)</script>', html_s, re.S).group()
        live = re.search(r'isLive', room_info)
        if live:
            self.live_status = re.search(r'[\'\"]?isLive[\'\"]? ?: ?[\'\"]?(\d)[\'\"]?', room_info).group(1)
            self.ch_name = re.search(r'[\'\"]?anchorName[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', room_info).group(1)
            self.title = re.search(r'[\'\"]?title[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', room_info).group(1)
            self.title = self.title.replace('\\u0026', '&')
        else:
            self.live_status = '0'
