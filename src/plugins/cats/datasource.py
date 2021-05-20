import json

from .model import PictureSource


class CatPicture(PictureSource):
    @classmethod
    def api_url(cls) -> str:
        # https://thecatapi.com
        return 'https://api.thecatapi.com/v1/images/search'

    @classmethod
    async def resolve(cls, content: bytes) -> str:
        return json.loads(content)[0]['url']
