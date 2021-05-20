import asyncio
from typing import List, Optional

import pytest
import websockets

import nonebot
import uvicorn
from fastapi import FastAPI
from nonebot.adapters.cqhttp import Bot

from message import self_id


class UvicornTestServer(uvicorn.Server):
    _serve_task: asyncio.Task

    def __init__(self, app, host='localhost', port=8080):
        self._startup_done = asyncio.Event()
        super().__init__(config=uvicorn.Config(app, host=host, port=port))

    async def startup(self, sockets: Optional[List] = None) -> None:
        await super().startup(sockets=sockets)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def up(self) -> None:
        self._serve_task = asyncio.create_task(self.serve())
        await self._startup_done.wait()

    async def down(self) -> None:
        self.should_exit = True
        await self._serve_task


@pytest.fixture(scope='session')
def event_loop():
    nonebot.init()
    app: FastAPI = nonebot.get_asgi()
    driver = nonebot.get_driver()
    driver.register_adapter("cqhttp", Bot)

    nonebot.load_plugins('src/plugins')

    server = UvicornTestServer(app)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.up())
    yield loop
    loop.run_until_complete(server.down())
    loop.close()


@pytest.fixture
def websocket(event_loop):
    headers = {'X-Self-ID': str(self_id)}
    url = 'ws://127.0.0.1:8080/cqhttp/ws'
    client: websockets.WebSocketClientProtocol = event_loop.run_until_complete(
        websockets.connect(url, extra_headers=headers, loop=event_loop))
    yield client
    event_loop.run_until_complete(client.close())
