from typing import List, Set

import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):
    setu_maximum: int = 3  # 警告: 不宜过大
    data_path: str = "data"
    setu_proxy: str = None
    setu_r18: int = 0
    setu_check_size: bool = False
    setu_share_cd: bool = False
    setu_blacklist: Set[str] = {'R-18'}

    class Config:
        extra = "ignore"


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
