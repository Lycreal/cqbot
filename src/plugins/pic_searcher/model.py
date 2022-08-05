import urllib.parse

from .saucenao import get_saucenao_detail


class PicSearcher:
    @classmethod
    async def do_search(cls, image: str, site: str = 'saucenao') -> str:
        try:
            if site == 'saucenao':
                reply: str = await cls.do_search_saucenao(image)
            else:
                reply = await cls.do_search_saucenao(image)
        except Exception as e:
            import traceback
            reply = '处理异常：{}'.format("\n".join(traceback.format_exception_only(type(e), e)))
        return reply

    @classmethod
    async def do_search_saucenao(cls, img_url: str) -> str:
        try:
            results = await get_saucenao_detail(img_url)

            for result in [result for result in results if cls.float(result.Similarity) > 0.9]:
                if cls.check_pixiv_url(result.URL):
                    break
            else:
                if results and cls.float(results[0].Similarity) > 0.6:
                    result = results[0]
                else:
                    result = None

            if result:
                result.URL = cls.shorten_pixiv_url(result.URL)
                reply = str(result)
            else:
                reply = '未找到相似图片\n'
        except Exception as e:
            import traceback
            traceback.print_exc()
            reply = '\n'.join(traceback.format_exception_only(type(e), e))
        return reply.strip()

    @staticmethod
    def float(string: str) -> float:
        """百分数转为int"""
        if string.endswith('%'):
            return float(string.rstrip("%")) / 100
        else:
            return float(string)

    @staticmethod
    def check_pixiv_url(url: str) -> bool:
        parse = urllib.parse.urlparse(url)
        return bool(parse.hostname and 'pixiv' in parse.hostname)

    @staticmethod
    def shorten_pixiv_url(url: str) -> str:
        parse = urllib.parse.urlparse(url)
        if parse.hostname and 'pixiv' in parse.hostname:
            querys = dict(urllib.parse.parse_qsl(parse.query))
            illust_id = querys.get('illust_id')
            if illust_id:
                return f'https://www.pixiv.net/artworks/{illust_id}'
        return url
