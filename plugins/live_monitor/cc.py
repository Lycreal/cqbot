import re
from plugins.live_monitor.general import Channel


class NetEaseChannel(Channel):
    def __init__(self, id: str, name: str):
        super(NetEaseChannel, self).__init__()
        self.live_url = f'http://cc.163.com/{id}/'
        self.api_url = self.live_url

    def resolve(self, html_s):
        room_info = re.search(r'<script type="text/javascript">\s+var roomInfo(.*?)</script>', html_s, re.S).group()
        live = re.search(r'isLive', room_info)
        if live:
            self.live_status = re.search(r'[\'\"]?isLive[\'\"]? ?: ?[\'\"]?(\d)[\'\"]?', room_info).group(1)
            # self.name = re.search(r'[\'\"]?anchorName[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', room_info).group(1)
            self.title = re.search(r'[\'\"]?title[\'\"]? ?: ?[\'\"]?([^\'\"]+)[\'\"]?', room_info).group(1)
        else:
            self.live_status = '0'


def main():
    quin = NetEaseChannel('361433', '')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
