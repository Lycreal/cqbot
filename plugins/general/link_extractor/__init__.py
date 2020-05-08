import re
import html
import json
import asyncio
import aiohttp
import lxml.html
import urllib.parse
from typing import List, Dict, Optional
from nonebot import on_natural_language, NLPSession

__plugin_name__ = 'B站小程序解析'
__plugin_usage__ = r'''自动解析B站小程序分享链接，显示视频标题并推测视频链接'''


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    def shorten(_url: str) -> str:
        url_patterns = (
            re.compile(r'/(av\d+|BV\w+)'),
            re.compile(r'/(ep\d+)'),
            re.compile(r'b23.tv/(\w+)'),
        )
        for p in url_patterns:
            vid = p.search(_url)
            if vid:
                _url = f'https://b23.tv/{vid[1]}'
                break
        return _url

    ctx: dict = session.ctx
    msg_list: List[Dict] = ctx.get('message')

    for msg in msg_list:
        if msg['type'] == 'rich' and html.unescape(msg['data'].get('title')) == '[QQ小程序]哔哩哔哩':
            # 提取分享标题
            content = json.loads(html.unescape(msg['data']['content']))
            title: str = content['detail_1']['desc']
            msg = title + '\n'

            url = content['detail_1'].get('qqdocurl', '')
            if not url:
                url = await search_bili_by_title(title)

            if url:
                msg += shorten(url)
            else:
                msg += '未找到视频地址'

            await session.send(msg)


async def search_bili_by_title(title: str) -> Optional[str]:
    """
    :param title:
    :return: url
    :rtype: Optional[str]
    """
    # remove brackets
    brackets_pattern = re.compile(r'[()\[\]{}（）【】]')
    title_without_brackets = brackets_pattern.sub(' ', title).strip()
    search_url = f'https://search.bilibili.com/video?keyword={urllib.parse.quote(title_without_brackets)}'

    try:
        async with aiohttp.request('GET', search_url, timeout=aiohttp.client.ClientTimeout(10)) as resp:
            text = await resp.text(encoding='utf8')
            content: lxml.html.HtmlElement = lxml.html.fromstring(text)
    except asyncio.TimeoutError:
        return None

    for video in content.xpath('//li[@class="video-item matrix"]/a[@class="img-anchor"]'):
        if title == ''.join(video.xpath('./attribute::title')):
            url = ''.join(video.xpath('./attribute::href'))
            break
    else:
        url = None
    return url
