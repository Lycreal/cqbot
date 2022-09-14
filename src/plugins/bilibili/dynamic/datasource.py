import json
from collections import namedtuple
from typing import List, Dict, Optional, Any, Tuple, Union

import httpx

# {uid:dynamic_id}
LAST: Dict[str, int] = {}

Resp = namedtuple('Resp', 'name msg imgs dynamic_id')


async def getDynamicStatus(uid: str, debug: int = 0) -> Optional[Resp]:
    cards_data = await getCards(uid)

    last_dynamic = LAST.setdefault(uid, cards_data[0]['desc']['dynamic_id'])

    for i, card_data in enumerate(cards_data):
        if last_dynamic >= card_data['desc']['dynamic_id']:
            break

    if debug:
        i = debug

    if i >= 1:
        LAST[uid] = cards_data[i - 1]['desc']['dynamic_id']
        return CardData(cards_data[i - 1]).resolve()
    else:
        return None  # 没有新动态


async def getCards(uid: str) -> List[Dict[str, Any]]:
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    params = {
        'host_uid': str(uid),
        'offset_dynamic_id': '0'
    }
    async with httpx.AsyncClient() as client:  # type: httpx.AsyncClient
        resp = await client.get(url, params=params)
        res = await resp.aread()
    cards_data = json.loads(res)
    return cards_data['data']['cards']


class CardData(Dict[str, Any]):
    def __init__(self, obj: Any) -> None:
        super(CardData, self).__init__(obj)
        self['card'] = deep_decode(self['card'])

    def resolve(self) -> Resp:
        name = self["desc"]["user_profile"]["info"]["uname"]
        c_type = self['desc']['type']

        msg, imgs = self.resolve_card(self['card'], name, c_type)

        # 如果太长，裁剪
        if len(msg) > 130:
            msg = msg[:120] + f'... (剩余{len(msg) - 120}字)'

        if len(imgs) > 2:
            msg += f'(共{len(imgs)}张图片)'

        return Resp(name, msg, [imgs[0]], self['desc']['dynamic_id'])

    @staticmethod
    def resolve_card(card: Dict[str, Any], name: str, c_type: int) -> Tuple[str, List[str]]:
        try:
            if c_type == 1:  # 转发
                content = card['item'].get('content')
                msg = f'(转发){name}：{content}\n{"=" * 20}\n'

                origin_type = card['item']['orig_type']
                if origin_type != 1024:  # 没有被删
                    origin_name = card['origin_user']['info']['uname']
                    msg_a, img_urls = CardData.resolve_card(card['origin'], origin_name, origin_type)
                else:  # 被删了, 一般不会发生
                    msg_a, img_urls = card['item']['tips'], []
                msg += msg_a
            elif c_type == 2:  # 图片动态
                description = card['item'].get('description')
                msg = f'(动态){name}：\n{description}'
                img_urls = [pic_info['img_src'] for pic_info in card['item']['pictures']]
            elif c_type == 4:  # 文字动态
                content = card['item'].get('content')
                msg = f'(动态){name}：\n{content}'
                img_urls = []
            elif c_type == 8:  # 视频动态
                dynamic = card.get('dynamic')
                title = card.get('title')
                pic = card.get('pic')
                msg = f'(视频){name}：《{title}》\n{dynamic}'
                img_urls = [pic]
            elif c_type == 64:  # 专栏动态
                dynamic = card.get('dynamic', '')
                title = card.get('title')
                banner_url = card.get('banner_url')
                msg = f'(专栏){name}：《{title}》\n{dynamic}'
                img_urls = [banner_url]
            elif c_type == 256:  # 音乐动态
                title = card.get('title')
                intro = card.get('intro')
                cover = card.get('cover')
                msg = f'(音乐){name}：《{title}》\n{intro}'
                img_urls = [cover]
            elif c_type == 2048:  # 特殊动态类型（头像框、直播日历等）
                content = card['vest'].get('content')
                title = card['sketch'].get('title')
                msg = f'(动态){name}：{content}\n{title}'
                img_urls = []
            elif c_type == 4200:  # 直播间动态
                roomid = card.get('roomid')
                cover = card.get('user_cover') or card.get('cover')
                title = card.get('title')
                msg = f'(直播){name}：{title} https://live.bilibili.com/{roomid}'
                img_urls = [cover]
            else:  # 未知
                msg = f'{name}：(未知动态类型{c_type})'
                img_urls = []
        except (TypeError, KeyError):
            msg = f'{name}：(动态类型{c_type}，解析失败)'
            img_urls = []
        if not msg.endswith('\n') and img_urls:
            msg += '\n'
        return msg, img_urls


def deep_decode(j: Union[Dict[str, Any], List[Any], str]) -> Union[Dict[str, Any], List[Any], str]:
    """将str完全解析为json"""
    if isinstance(j, dict):
        j = j.copy()
        for k, v in j.items():
            j[k] = deep_decode(v)
    elif isinstance(j, list):
        j = j.copy()
        for i, v in enumerate(j):
            j[i] = deep_decode(v)
    elif isinstance(j, str):
        try:
            j = deep_decode(json.loads(j))
        except json.decoder.JSONDecodeError:
            pass
    return j
