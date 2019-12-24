import re
import json
import lxml.html
from . import BaseChannel


class NetEaseChannel(BaseChannel):
    def set_url(self):
        self.live_url = f'https://cc.163.com/{self.cid}/'
        self.api_url = self.live_url

    def resolve(self, html_s):
        html_element: lxml.html.HtmlElement = lxml.html.fromstring(html_s)
        try:
            script = html_element.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
            room_info = json.loads(script)['props']['pageProps']['roomInfoInitData']['live']

            self.title = room_info['title']
            hot_score = room_info['hot_score']
            self.live_status = '1' if hot_score > 0 else '0'
        except IndexError:
            script = html_element.xpath('//script[contains(text(),"var roomInfo")]/text()')[0]
            # room_info = re.search(r'var roomInfo(.*?);', html_s, re.S).group()
            live = re.search(r'isLive', script)
            if live:
                self.live_status = re.search(r'[\'\"]?isLive[\'\"]? ?: ?[\'\"]?(\d)[\'\"]?', script).group(1)
                self.ch_name = re.search(r'[\'\"]?anchorName[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', script).group(1)
                title = re.search(r'[\'\"]?title[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', script).group(1)
                self.title = title.replace('\\u0026', '&')
            else:
                self.live_status = '0'
