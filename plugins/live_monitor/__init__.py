__all__ = ['bili', 'cc', 'general', 'youtube']

from plugins.live_monitor.general import Channel as GeneralChannel
from plugins.live_monitor.youtube import YoutubeChannel
from plugins.live_monitor.bili import BiliChannel
from plugins.live_monitor.cc import NetEaseChannel
import time


def init_channel(type: str, id: str, name: str):
    if type == 'bili':
        return BiliChannel(id, name)
    elif type == 'you':
        return YoutubeChannel(id, name)
    elif type == 'cc':
        return NetEaseChannel(id, name)
    else:
        return KeyError(type)


class Monitor:
    channel_list: list = []
    debug = False
    pos = -1
    notify = print

    def __init__(self, channel_type, debug=False):
        self.channel_type = channel_type
        self.debug = debug

    def add(self, ch_list):
        for ch_info in ch_list:
            ch = init_channel(self.channel_type, *ch_info)
            if ch.id not in [ch.id for ch in self.channel_list]:
                self.channel_list.append(ch)

    def load(self):
        pass

    def save(self):
        pass

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


if __name__ == '__main__':
    monitor = Monitor('you', debug=True)
    monitor.add([('UCdn5BQ06XqgXoAxIhbqw5Rg', 'FBK')])
    monitor.add([('UCveZ9Ic1VtcXbsyaBgxPMvg', 'meiji')])
    while True:
        monitor.run()
        time.sleep(10)
