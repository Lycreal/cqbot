import typing as T
from datetime import datetime, timedelta
from random import randint

import cv2
import numpy as np
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
    image = cv2.imdecode(np.asarray(bytearray(image_bytes)), cv2.IMREAD_COLOR)
    image[0, 0] = randint(0, 255)
    image[0, -1] = randint(0, 255)
    image[-1, 0] = randint(0, 255)
    image[-1, -1] = randint(0, 255)
    return cv2.imencode('.png', image)[1]


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
