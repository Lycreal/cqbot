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

    def __init__(self, app, host='127.0.0.1', port=13695):
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
