__all__ = ['bili', 'cc', 'general', 'youtube']

from .general import Channel as GeneralChannel
from .youtube import YoutubeChannel
from .bili import BiliChannel
from .cc import NetEaseChannel


def init_channel(type: str, id: str, name: str):
    if type == 'bili':
        return BiliChannel(id, name)
    elif type == 'you':
        return YoutubeChannel(id, name)
    elif type == 'cc':
        return NetEaseChannel(id, name)
    else:
        return KeyError(type)
