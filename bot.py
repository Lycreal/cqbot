import logging
import nonebot
from nonebot.log import logger
import config_bot

if __name__ == '__main__':
    nonebot.init(config_bot)
    logger.setLevel(logging.INFO)
    nonebot.load_plugins(
        str(config_bot.root_path / 'plugins'),
        'plugins'
    )
    logger.info('Starting')
    nonebot.run()
