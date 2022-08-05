# https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-local-per-directory-plugins
import asyncio
import os
from typing import Dict

import pytest
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Bot
from starlette.testclient import TestClient

from .message import NewNumber

os.environ['COMMAND_START'] = '["/", ""]'
os.environ['SUPERUSERS'] = "[222222]"
os.environ['moderatecontent_apikey'] = 'abc'


@pytest.fixture(scope="session")
def client() -> TestClient:
    from bot import app
    client = TestClient(app)
    return client


@pytest.fixture(scope="function")
def bot(client: TestClient, monkeypatch) -> Bot:
    data_seq = []

    async def send_msg(self, **data) -> Dict[str, int]:
        data_seq.append(data)
        return {'message_id': 123}

    async def delete_msg(self, **data) -> None:
        data_seq.append(data)

    async def fetch(self):
        while not data_seq:
            await asyncio.sleep(0.1)
        return data_seq.pop()

    setattr(Bot, 'send_msg', send_msg)
    setattr(Bot, 'delete_msg', delete_msg)
    setattr(Bot, 'fetch', fetch)

    self_id = str(NewNumber.self_id())
    with client.websocket_connect(url='/onebot/v11/ws', headers={'X-Self-ID': self_id}):
        while True:
            bot = get_bots().get(self_id)
            if bot:
                break
        yield bot
