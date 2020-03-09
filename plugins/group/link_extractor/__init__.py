import re
import html
import json
import aiohttp
import difflib
import lxml.html
import urllib.parse
from typing import List, Dict, Tuple
from nonebot import on_natural_language, NLPSession

__plugin_name__ = 'B站小程序解析'
__plugin_usage__ = r'''解析B站小程序分享链接，显示视频标题并推测视频链接'''


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    ctx: dict = session.ctx
    msg_list: List[Dict] = ctx.get('message')

    for msg in msg_list:
        if msg['type'] == 'rich' and html.unescape(msg['data'].get('title')) == '[QQ小程序]哔哩哔哩':
            content = json.loads(html.unescape(msg['data']['content']))
            title: str = content['detail_1']['desc']

            videos = await search_bili_by_title(title)

            # 构建消息内容
            msg = title
            match_title: List[str] = difflib.get_close_matches(title, [v[1] for v in videos], n=3, cutoff=1)
            if not match_title:
                match_title = difflib.get_close_matches(title, [v[1] for v in videos], n=3, cutoff=0.6)
            if not match_title:
                return

            match_vid = [v[0] for v in videos if v[1] == match_title]
            for vid in match_vid:
                msg += f'\nhttps://www.bilibili.com/video/av{vid}'
            if len(match_vid) >= 1 or title != match_title[0]:
                msg += f'\n（视频地址为推测）'
            await session.send(msg)


async def search_bili_by_title(title: str) -> List[Tuple[str, str]]:
    """
    :param title:
    :return: [(av号,标题)]
    :rtype: List[Tuple[str, str]]
    """
    search_url = f'https://search.bilibili.com/video?keyword={urllib.parse.quote(title)}'
    async with aiohttp.request('GET', search_url) as resp:
        text = await resp.text(encoding='utf8')
        content: lxml.html.HtmlElement = lxml.html.fromstring(text)

    av_pattern = re.compile('www.bilibili.com/video/av([0-9]+)')
    videos: List[Tuple[str, str]] = [
        (av_pattern.search(video.xpath('./attribute::href')[0]).group(1),
         video.xpath('./attribute::title')[0])
        for video in content.xpath('//li[@class="video-item matrix"]/a[@class="img-anchor"]')
    ]
    return videos
