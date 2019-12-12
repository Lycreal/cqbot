import logging
from os import path

import nonebot
from nonebot.log import logger
import config_bot

root_path = path.dirname(__file__)
if __name__ == '__main__':
    nonebot.init(config_bot)
    logger.setLevel(logging.INFO)
    nonebot.load_plugins(
        path.join(root_path, 'plugins'),
        'plugins'
    )
    logger.info('Starting')
    nonebot.run()
