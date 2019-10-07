from plugins.live_monitor.general import BaseChannel
from plugins.live_monitor.youtube import YoutubeChannel
from plugins.live_monitor.bili import BiliChannel
from plugins.live_monitor.cc import NetEaseChannel
import json
from typing import List, Union, Tuple


class Monitor:
    def __init__(self, channel_type: str, debug=False):
        assert channel_type in ['bili', 'you', 'cc']
        self.channel_list: List[BaseChannel] = []
        self.pos = -1
        self.channel_type = channel_type
        self.DEBUG = debug

    def init_channel(self, cid: str, name: str):
        if self.channel_type == 'bili':
            return BiliChannel(cid, name)
        elif self.channel_type == 'you':
            return YoutubeChannel(cid, name)
        elif self.channel_type == 'cc':
            return NetEaseChannel(cid, name)

    def add(self, cid: str, name: str, group: Union[str, List[str]]):
        if type(group) == list:
            ret = [self.add(cid, name, group_) for group_ in group]
            return 0 not in ret

        group: str
        for channel in self.channel_list:
            if channel.cid == cid:
                if name:
                    channel.name = name
                if group not in channel.sendto:
                    channel.sendto.append(group)
                    return 2  # 添加新sendto
                elif name:
                    return 3  # 名称已修改
                else:
                    return 0  # 已存在
                # break
        else:
            ch = self.init_channel(cid, name)
            ch.sendto = [group]
            self.channel_list.append(ch)
            return 1  # 添加新频道

    def remove(self, cid: str):
        for ch in self.channel_list:
            if ch.cid == cid:
                self.channel_list.remove(ch)

    def load(self):
        try:
            with open(self.channel_type + '.json', 'r') as f:
                channel_json = json.load(f)
            [self.add(ch_j['cid'], ch_j['name'], ch_j['groups']) for ch_j in channel_json]
        except FileNotFoundError:
            pass

    def save(self):
        channel_json = [{'cid': ch.cid, 'name': ch.name, 'groups': ch.sendto} for ch in self.channel_list]
        with open(self.channel_type + '.json', 'w') as f:
            json.dump(channel_json, f, indent=2, ensure_ascii=False)

    def next(self):
        if self.channel_list:
            self.pos = self.pos + 1 if self.pos < len(self.channel_list) - 1 else 0
            return self.channel_list[self.pos]
        else:
            return None

    def run(self) -> Tuple[List, str]:
        channel: BaseChannel = self.next()
        if channel and channel.sendto and (channel.update() or self.DEBUG):
            return channel.sendto, channel.notify()
        else:
            return channel.sendto, ''

    def __str__(self):
        msg = ''
        for ch in self.channel_list:
            msg += f'{ch.name}:{ch.live_status}'
        return msg
