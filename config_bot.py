from pathlib import Path
from nonebot.default_config import *

SUPERUSERS = set()

NICKNAME = {'机器人', '复读机', 'bot', 'Bot'}
COMMAND_START = {'.', '。', '!', '！'}
COMMAND_SEP = {'.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=1)
SESSION_RUN_TIMEOUT = timedelta(seconds=20)
HOST = '0.0.0.0'
PORT = 8080

APSCHEDULER_CONFIG = {
    'executors': {
        'default': {'type': 'processpool', 'max_workers': 10}
    },
    'job_defaults': {
        'coalesce': False,
        'max_instances': 5
    },
    'timezone': 'Asia/Shanghai'
}

root_path: Path = Path(__file__).parent
data_path: Path = root_path.joinpath('data')
