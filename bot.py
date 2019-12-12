import logging
from os import path

import nonebot
from nonebot.log import logger
import config_bot

if __name__ == '__main__':
    nonebot.init(config_bot)
    logger.setLevel(logging.INFO)
    root_path = path.dirname(__file__)
    nonebot.load_plugins(
        path.join(root_path, 'plugins'),
        'plugins'
    )
    logger.info('Starting')
    nonebot.run()
