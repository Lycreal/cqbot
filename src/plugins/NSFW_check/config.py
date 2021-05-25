import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    sightengine_api_user: str = ''
    sightengine_api_secret: str = ''

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
