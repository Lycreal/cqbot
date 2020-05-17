import asyncio
import aiohttp.client
import lxml.html
from nonebot import on_command, CommandSession
from nonebot.command.argfilter import extractors, validators, controllers

__plugin_name__ = '搜图'
__plugin_usage__ = r'''搜索P站图片 关键词：stu st
输入命令后发送要搜索的图片
例：
.st <图片> （有空格）
.st （发送命令后发送图片）
'''


@on_command('st', aliases=('stu',), only_to_me=False)
async def search_pic(session: CommandSession):
    img_url: str = session.get(
        'img_url', prompt='请发送要搜索的图片',
        arg_filters=[
            controllers.handle_cancellation(session),
            extractors.extract_image_urls,
            validators.not_empty('请发送图片')
        ]
    )[0]
    await session.send(await do_search(img_url), at_sender=True)


@search_pic.args_parser
async def _(session: CommandSession):
    image_urls = extractors.extract_image_urls(session.ctx['message'])
    if image_urls:
        session.state['img_url'] = image_urls


async def do_search(url: str):
    # saucenao
    s_url = f'https://saucenao.com/search.php?url={url}'

    task = asyncio.create_task(shorten_img_url(url))
    s_info = await get_saucenao_detail(s_url)

    if s_info and percent_to_int(s_info[0]['Similarity']) > 0.6:
        task.cancel()
        msg = ''
        for k, v in s_info[0].items():
            if k != 'Content':
                msg += f'{k}: {v}\n'
            else:
                msg += f'{v}\n'
        return msg.strip()
    else:
        tmp_link = (await asyncio.gather(task))[0]
        msg = '未找到相似图片，其他搜图引擎：\n'
        msg += f'①https://iqdb.org/?url={tmp_link}\n'
        msg += f'②https://ascii2d.net/search/url/{tmp_link}\n'
        msg += f'③https://www.google.com/searchbyimage?image_url={tmp_link}&safe=off\n'
        return msg.strip()


async def get_saucenao_detail(s_url):
    async with aiohttp.client.request('GET', s_url) as resp:
        text = await resp.text(encoding='utf8')

    html_e: lxml.html.HtmlElement = lxml.html.fromstring(text)
    results = [
        {
            'Similarity': ''.join(
                r.xpath('.//div[@class="resultsimilarityinfo"]/text()')),
            'Title': ''.join(
                r.xpath('.//div[@class="resulttitle"]/descendant-or-self::text()')),
            'Content': '\n'.join(
                r.xpath('.//div[@class="resultcontentcolumn"]/descendant-or-self::text()')).replace(': \n', ': '),
            'URL': ''.join(
                r.xpath('.//div[@class="resultcontentcolumn"]/a[1]/attribute::href')),
        }
        for r in html_e.xpath('//div[@class="result"]/table[@class="resulttable"]')
    ]
    return results


# 百分数转为int
def percent_to_int(string):
    if string.endswith('%'):
        return float(string.rstrip("%")) / 100
    else:
        return float(string)


async def shorten_img_url(url: str):
    i_url = f'https://iqdb.org/?url={url}'
    async with aiohttp.client.request('GET', i_url) as resp:
        text = await resp.text(encoding='utf8')

    html_e: lxml.html.HtmlElement = lxml.html.fromstring(text)
    img_uri = html_e.xpath('//img[contains(attribute::src,"/thu/thu_")]/attribute::src')[0]
    img_url = f'https://iqdb.org{img_uri}'
    return img_url
