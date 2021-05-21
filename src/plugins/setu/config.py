from pydantic import BaseSettings
import nonebot


class Config(BaseSettings):
    debug: bool = False
    setu_maximum: int = 3
    data_path: str = "userdata"
    setu_apikey: str = ""
    setu_proxy: str = None
    setu_r18: int = 0
    setu_check_size: bool = False
    setu_share_cd: bool = False

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
