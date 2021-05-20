import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    # plugin custom config
    cats_api_timeout: float = 10

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
