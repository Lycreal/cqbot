import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    picsearcher_debug: bool = False

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
