from plugins.live_monitor.general import BaseChannel
from plugins.live_monitor.youtube import YoutubeChannel
from plugins.live_monitor.bili import BiliChannel
from plugins.live_monitor.cc import NetEaseChannel
import json
import pathlib
from typing import List, Union, Tuple


class Monitor:
    def __init__(self, channel_type: str, debug=False):
        assert channel_type in ['bili', 'you', 'cc']
        self.save_file = pathlib.Path('data').joinpath(f'{self.channel_type}.json')
        self.channel_list: List[BaseChannel] = []
        self.pos = -1
        self.channel_type = channel_type
        self.DEBUG = debug

    def init_channel(self, cid: str, name: str):
        if self.channel_type == 'bili':
            assert cid.isdecimal()
            return BiliChannel(cid, name)
        elif self.channel_type == 'you':
            assert len(cid) == 24
            assert cid.startswith('UC')
            return YoutubeChannel(cid, name)
        elif self.channel_type == 'cc':
            assert cid.isdecimal()
            return NetEaseChannel(cid, name)

    def add(self, cid: str, name: str, group: Union[str, List[str]]):
        if type(group) == list:
            ret = [self.add(cid, name, group_) for group_ in group]
            return ret

        group: str
        for channel in self.channel_list:
            if channel.cid == cid:
                if name:
                    channel.name = name
                if group not in channel.sendto:
                    channel.sendto.append(group)
                    return channel  # 添加新sendto
                elif name:
                    return 3  # 名称已修改
                else:
                    return 0  # 已存在
                # break
        else:
            ch = self.init_channel(cid, name)
            ch.sendto = [group]
            self.channel_list.append(ch)
            return ch  # 添加新频道

    def remove(self, cid: str, group: str):
        ret = 0
        for ch in self.channel_list:
            if ch.cid == cid:
                if group in ch.sendto:
                    ch.sendto.remove(group)
                    ret = 1
                    if not ch.sendto:
                        self.channel_list.remove(ch)
        return ret

    def load(self):
        if self.save_file.exists():
            with self.save_file.open('r', encoding='utf8') as f:
                channel_json = json.load(f)
            [self.add(ch_j['cid'], ch_j['name'], ch_j['groups']) for ch_j in channel_json]
        else:
            self.save()

    def save(self):
        channel_json = [{'cid': ch.cid, 'name': ch.name, 'groups': ch.sendto} for ch in self.channel_list]
        with self.save_file.open('w', encoding='utf8') as f:
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
