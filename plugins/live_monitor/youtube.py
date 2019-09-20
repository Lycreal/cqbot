import re
from plugins.live_monitor.general import Channel

# import requests
import ast
import json


class YoutubeChannel(Channel):
    def get_url(self):
        self.api_url = f'https://www.youtube.com/channel/{self.id}/live'
        self.live_url = self.api_url

    def resolve(self, html_s):
        content = re.search(r'.*RELATED_PLAYER_ARGS.*', html_s).group()
        with open(self.name, 'w', encoding='utf8') as f:
            f.write(content)
        if re.search(r'Last streamed live', content) or re.search(r'Streamed live', content):
            self.live_status = '0'
        elif re.search(r'Scheduled for', content):
            self.live_status = '2'
        elif re.search(r'Started streaming', content):
            self.live_status = '1'
        else:
            raise KeyError('找不到关键字')
        self.get_title(content)

    # def get_status(self):
    #     html_s = requests.get(self.api_url, proxies={'https': 'socks5://127.0.0.1:10808'}).text
    #     self.resolve(html_s)

    def get_title(self, content):
        match = re.search(r'\\"shareVideoEndpoint\\":{(.*?)}},', content)
        if match:
            text = '{%s}' % match.group(1)
            text_f = ast.literal_eval("'{}'".format(text))
            shareVideoEndpoint = json.loads(text_f)
            self.title = shareVideoEndpoint['videoTitle']
            self.live_url = shareVideoEndpoint['videoShareUrl']


def main():
    quin = YoutubeChannel('UC1opHUrw8rvnsadT-iGp7Cg', 'aqua')
    # quin = YoutubeChannel('UCWCc8tO-uUl_7SJXIKJACMw', 'mea')
    # quin = YoutubeChannel('UCn14Z641OthNps7vppBvZFA', '千草はな')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
