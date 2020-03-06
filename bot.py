import logging
import nonebot
from nonebot.log import logger
import config_bot

if __name__ == '__main__':
    nonebot.init(config_bot)
    logger.setLevel(logging.INFO)
    for dir_ in config_bot.root_path.joinpath('plugins').iterdir():
        if dir_.is_dir() and dir_.name != 'disabled':
            nonebot.load_plugins(str(dir_), f'plugins.{dir_.name}')
    logger.info('Starting')
    nonebot.run()
