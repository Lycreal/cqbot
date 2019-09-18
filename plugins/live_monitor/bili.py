from .general import Channel
import json


class BiliChannel(Channel):
    def __init__(self, id: str, name: str):
        super(BiliChannel, self).__init__()
        self.live_url = f'https://live.bilibili.com/{id}'
        self.api_url = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={id}'
        self.name = name

    def resolve(self, html_s):
        json_d = json.loads(html_s)
        self.live_status = str(json_d['data']['live_status'])
        self.title = json_d['data']['title']


def main():
    quin = BiliChannel('21224291', 'kky')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
