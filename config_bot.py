from nonebot.default_config import *
from config_private import SUPERUSERS, GROUPS

if not SUPERUSERS:
    SUPERUSERS = {}
NICKNAME = {'机器人', '复读机'}
COMMAND_START = {'.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=1)

HOST = '172.17.0.1'
PORT = 8080

if not GROUPS:
    GROUPS = []

APSCHEDULER_CONFIG = {
    'apscheduler.timezone': 'Asia/Shanghai',
    'apscheduler.job_defaults.max_instances': '5'
}
