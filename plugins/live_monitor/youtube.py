import re
from plugins.live_monitor.general import Channel


class YoutubeChannel(Channel):
    def __init__(self, id: str, name: str):
        super(YoutubeChannel, self).__init__()
        self.api_url = f'https://www.youtube.com/channel/{id}/live'
        self.live_url = self.api_url
        self.name = name

    def resolve(self, html_s):
        videoId = re.search(r'<meta itemprop="videoId" content="([^"]*)">', html_s).group(1)
        self.live_url = f'https://www.youtube.com/watch?v={videoId}'

        content = re.search(r'.*RELATED_PLAYER_ARGS.*', html_s).group()
        if re.search(r'Last streamed live', content) or re.search(r'Streamed live', content):
            self.live_status = '0'
        elif re.search(r'Scheduled for', content):
            self.live_status = '2'
        elif re.search(r'Started streaming', content):
            self.live_status = '1'
        else:
            raise KeyError('找不到关键字')
        self.title = re.search(r'\\"videoTitle\\":\\"([^\\]*)\\"', content).group(1)


def main():
    quin = YoutubeChannel('UC1opHUrw8rvnsadT-iGp7Cg', 'aqua')
    # quin = YoutubeChannel('UCWCc8tO-uUl_7SJXIKJACMw', 'mea')
    # quin = YoutubeChannel('UCn14Z641OthNps7vppBvZFA', '千草はな')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
