import re
from plugins.live_monitor.general import Channel

# import socks
# import socket


class YoutubeChannel(Channel):
    def __init__(self, id: str, name: str):
        super(YoutubeChannel, self).__init__()
        self.api_url = f'https://www.youtube.com/channel/{id}/live'
        self.live_url = self.api_url
        self.name = name

    def resolve(self, html_s):
        content = re.search(r'.*RELATED_PLAYER_ARGS.*', html_s).group()
        if not re.search(r'Scheduled for', content) and re.search(r'\\"isLive\\":true', content):
            self.live_status = '1'
            self.title = re.search(r'\\"videoTitle\\":\\"([^\\]*)\\"', content).group(1)
            videoId = re.search(r'<meta itemprop="videoId" content="([^"]*)">', html_s).group(1)
            self.live_url = f'https://www.youtube.com/watch?v={videoId}'
        else:
            self.live_status = '0'
            self.title = ''
            self.live_url = self.api_url


def main():
    # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 10808)
    # socket.socket = socks.socksocket
    quin = YoutubeChannel('UC1opHUrw8rvnsadT-iGp7Cg', 'aqua')
    # quin = YoutubeChannel('UCWCc8tO-uUl_7SJXIKJACMw', 'mea')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
