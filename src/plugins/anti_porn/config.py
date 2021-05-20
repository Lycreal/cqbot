import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    # plugin custom config
    baidu_api_key: str = None
    baidu_secret_key: str = None
    baidu_access_token: str = None

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
