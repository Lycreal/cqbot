import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    # plugin custom config
    data_path: str = 'data'

    class Config:
        extra = "ignore"


nonebot.init()
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
