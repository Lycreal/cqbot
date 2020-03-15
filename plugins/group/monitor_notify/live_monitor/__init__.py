import json
from typing import List, Union, Callable
from config_bot import data_path
from .general import BaseChannel
from .youtube import YoutubeChannel
from .bili import BiliChannel
from .cc import NetEaseChannel

__all__ = ['Monitor', 'BaseChannel', 'BiliChannel', 'YoutubeChannel', 'NetEaseChannel']


class Monitor:
    def __init__(self, channel_type: str, debug=False):
        assert channel_type in ['bili', 'you', 'cc'], 'Fatal Error: wrong channel_type'
        self.channel_type = channel_type

        if not data_path.exists():
            data_path.mkdir()
        self.save_file = data_path.joinpath(f'{self.channel_type}.json')

        self.channel_list: List[BaseChannel] = []
        self.pos = -1
        self.DEBUG = debug

    def init_channel(self, cid: str, name: str) -> BaseChannel:
        if self.channel_type == 'bili':
            assert cid.isdecimal(), f'格式错误:{self.channel_type} {cid}'
            return BiliChannel(cid, name)
        elif self.channel_type == 'you':
            assert len(cid) == 24 and cid.startswith('UC'), f'格式错误:{self.channel_type} {cid}'
            return YoutubeChannel(cid, name)
        elif self.channel_type == 'cc':
            assert cid.isdecimal(), f'格式错误:{self.channel_type} {cid}'
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
                if group not in channel.targets:
                    channel.targets.append(group)
                    return channel  # 添加新target
                elif name:
                    return 3  # 名称已修改
                else:
                    return 0  # 已存在
                # break
        else:
            ch = self.init_channel(cid, name)
            ch.targets.append(group)
            self.channel_list.append(ch)
            return ch  # 添加新频道

    def remove(self, cid: str, group: str):
        ret = 0
        for ch in self.channel_list:
            if ch.cid == cid:
                if group in ch.targets:
                    ch.targets.remove(group)
                    ret = 1
                    if not ch.targets:
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
        channel_json = [{'cid': ch.cid,
                         'name': ch.name if ch.name else ch.ch_name,
                         'groups': ch.targets}
                        for ch in self.channel_list]
        with self.save_file.open('w', encoding='utf8') as f:
            json.dump(channel_json, f, indent=2, ensure_ascii=False)

    def next(self):
        if self.channel_list:
            self.pos = self.pos + 1 if self.pos < len(self.channel_list) - 1 else 0
            return self.channel_list[self.pos]
        else:
            return None

    async def run(self, func: Callable[[List[str], str], None]):
        channel: BaseChannel = self.next()
        if channel and channel.targets:
            if await channel.update() or self.DEBUG:
                func(channel.targets, channel.notify())

    def __str__(self):
        msg = ''
        for ch in self.channel_list:
            msg += f'{ch.name}:{ch.live_status}'
        return msg
