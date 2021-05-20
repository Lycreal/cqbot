import base64
from io import BytesIO
from typing import Dict, Any, Union
from pydantic import BaseModel
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import httpx
import PIL.Image


class AccessToken(BaseModel):
    api_key: str = None
    secret_key: str = None

    access_token: str = None
    expire_time: datetime = None

    def __str__(self) -> str:
        if not self.access_token or self.check_expired() is True:
            self.update_access_token()
        return self.access_token

    async def update_access_token(self) -> None:
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        # doc: http://ai.baidu.com/docs#/Auth
        if self.api_key is None or self.secret_key is None:
            raise ValueError('Must specific api_key and secret_key')

        host = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        async with httpx.AsyncClient() as client:  # type: httpx.AsyncClient
            response = await client.post(host, params=params)
            result: Dict[str, Any] = response.json()

        self.access_token = result.get('access_token')
        if 'expires_in' in result.keys():
            self.expire_time = datetime.now() + timedelta(seconds=result.get('expires_in'))

    def check_expired(self) -> bool:
        if self.expire_time:
            return bool(self.expire_time < datetime.now())
        else:
            return False


class AntiPorn(BaseModel):
    access_token: AccessToken

    async def check_image(self, image: Union[str, bytes, BytesIO, Path]) -> str:
        result = await self.do_check(self.get_body(image))

        if 'conclusion' in result.keys():
            msg: str = result['conclusion']
            if 'data' in result.keys():
                if sub_msg := '|'.join(d.get('msg') for d in result['data']):
                    msg += '|' + sub_msg
        else:
            msg = result.get('error_msg')
        return msg

    @staticmethod
    def get_body(image: Union[str, bytes, BytesIO, Path]) -> Dict[str, str]:
        if isinstance(image, str):
            parse = urlparse(image)
            if parse.scheme in ['http', 'https']:
                body = {"imgUrl": image}
            else:
                raise ValueError('Invalid imgUrl, support: http, https')
        else:
            if isinstance(image, bytes):
                img_bytes = image
                img: PIL.Image.Image = PIL.Image.open(BytesIO(img_bytes))
            elif isinstance(image, (BytesIO, Path)):
                img = PIL.Image.open(image)
                img_bytes = img.tobytes()
            else:
                raise TypeError('Image must be one of [str, bytes, BytesIO, Path]')
            img_base64 = base64.b64encode(img_bytes).decode()

            if not 5120 < len(img_base64) < 4182016:
                raise
            if 128 <= min(img.width, img.height) <= 4096:
                raise
            body = {"image": img_base64}
        return body

    async def do_check(self, body: Dict[str, str]) -> Dict[str, Any]:
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
        params = {'access_token': str(self.access_token)}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        async with httpx.AsyncClient() as client:  # type: httpx.AsyncClient
            response = await client.post(request_url, params=params, data=body, headers=headers, timeout=10)
            result: Dict[str, Any] = response.json()
        return result
