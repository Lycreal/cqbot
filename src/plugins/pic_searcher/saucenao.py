from typing import List

import httpx
import lxml.html
from pydantic import BaseModel

from .config import plugin_config

DEBUG = plugin_config.debug


class SaucenaoResult(BaseModel):
    Similarity: str
    Title: str
    Content: str
    URL: str

    def __str__(self) -> str:
        return '\n'.join(
            f'{k}: {v}' if k != 'Content' else v
            for k, v in self.dict().items()
        )


class SauceNAOError(Exception):
    pass


async def get_saucenao_detail(img_url: str) -> List[SaucenaoResult]:
    s_url = f'https://saucenao.com/search.php?url={img_url}'

    async with httpx.AsyncClient(timeout=10) as client:  # type: httpx.AsyncClient
        resp = await client.request('GET', s_url)
        content: bytes = await resp.aread()
    if DEBUG:
        with open('debug/saucenao.html', 'wb') as f:
            f.write(content)

    html_e: lxml.html.HtmlElement = lxml.html.fromstring(content)

    if 'Error' in ''.join(html_e.xpath('//title/text()')):
        text = ''.join(html_e.xpath('//body/text()')).strip()
        raise SauceNAOError(text)

    results = [
        SaucenaoResult(
            Similarity=''.join(r.xpath('.//div[@class="resultsimilarityinfo"]/text()')),
            Title=''.join(r.xpath('.//div[@class="resulttitle"]/descendant-or-self::text()')),
            Content='\n'.join(r.xpath('.//div[@class="resultcontentcolumn"]/descendant-or-self::text()')).replace(': \n', ': '),
            URL=''.join(r.xpath('.//div[@class="resultcontentcolumn"]/a[1]/attribute::href')),
        )
        for r in html_e.xpath('//div[@class="result"]/table[@class="resulttable"]')
    ]
    return results
