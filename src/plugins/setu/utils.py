import typing as T
from datetime import datetime, timedelta
from io import BytesIO
from random import randint

import PIL.Image
from pydantic import BaseModel


def shuzi2number(shuzi: T.Optional[str]) -> int:
    s = {'一': 1, '两': 2, '二': 2, '三': 3,
         '四': 4, '五': 5, '六': 6, '七': 7,
         '八': 8, '九': 9, '十': 10}
    if not shuzi:
        return 1
    elif shuzi.isdecimal():
        return int(shuzi)
    elif shuzi in s.keys():
        return s[shuzi]
    else:
        return 1


def shuffle(image_bytes: bytes) -> bytes:
    image: PIL.Image.Image = PIL.Image.open(BytesIO(image_bytes))
    pixels = image.load()
    i, j = image.size
    pixels[0, 0] = randint(0, 255)
    pixels[i, 0] = randint(0, 255)
    pixels[0, j] = randint(0, 255)
    pixels[i, j] = randint(0, 255)
    return image.tobytes()


class CoolDown(BaseModel):
    """example:
    cd = CoolDown(app='app1', td=20)
    cd.update(123)
    cd.check(123)
    """
    app: str
    td: float  # timedelta
    share: bool = False
    value: T.Dict[int, datetime] = {}

    def update(self, mid: int) -> None:
        if self.share:
            mid = 0
        self.value.update({mid: datetime.now()})

    def check(self, mid: int) -> bool:
        if self.share:
            mid = 0
        ret = datetime.now() >= self.value.get(mid, datetime.utcfromtimestamp(0)) + timedelta(seconds=self.td)
        return ret
