from nonebot.default_config import *

try:
    from config_private import SUPERUSERS
except ImportError:
    pass

NICKNAME = {'机器人', '复读机'}
COMMAND_START = {'.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=1)

HOST = '172.17.0.1'
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
