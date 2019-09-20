__all__ = ['bili', 'cc', 'general', 'youtube']

from plugins.live_monitor.general import Channel as GeneralChannel
from plugins.live_monitor.youtube import YoutubeChannel
from plugins.live_monitor.bili import BiliChannel
from plugins.live_monitor.cc import NetEaseChannel
import time
import json


class Monitor:
    channel_list: list = []
    debug = False
    pos = -1
    notify = print

    def __init__(self, channel_type: str, debug=False):
        assert channel_type in ['bili', 'you', 'cc']
        self.channel_type = channel_type
        self.debug = debug

    def init_channel(self, id: str, name: str):
        if self.channel_type == 'bili':
            return BiliChannel(id, name)
        elif self.channel_type == 'you':
            return YoutubeChannel(id, name)
        elif self.channel_type == 'cc':
            return NetEaseChannel(id, name)

    def add(self, id: str, name: str):
        ch = self.init_channel(id, name)
        if ch.id not in [ch.id for ch in self.channel_list]:
            self.channel_list.append(ch)

    def remove(self, id: str):
        for ch in self.channel_list:
            if ch.id == id:
                self.channel_list.remove(ch)

    def load(self):
        try:
            with open(self.channel_type + '.json', 'r') as f:
                channel_json = json.load(f)
            [self.add(ch_j['id'], ch_j['name']) for ch_j in channel_json]
        except FileNotFoundError:
            pass

    def save(self):
        channel_json = [{'id': ch.id, 'name': ch.name} for ch in self.channel_list]
        with open(self.channel_type + '.json', 'w') as f:
            json.dump(channel_json, f, indent=2)

    def next(self):
        if self.channel_list:
            self.pos = self.pos + 1 if self.pos < len(self.channel_list) - 1 else 0
            return self.channel_list[self.pos]
        else:
            return None

    def register_notifier(self, notify=print):
        self.notify = notify

    def run(self):
        channel: GeneralChannel = self.next()
        print(time.strftime('%H:%M:%S', time.localtime()))
        if channel.update() or self.debug:
            self.notify(channel)
            self.notify(channel.notify())
