import asyncio
from typing import List, Optional
import uvicorn
import pytest
import nonebot
from fastapi import FastAPI


class UvicornTestServer(uvicorn.Server):
    """Uvicorn test server

    Usage:
        @pytest.fixture
        server = UvicornTestServer()
        await server.up()
        yield
        await server.down()
    """
    _serve_task: asyncio.Task

    def __init__(self, app, host='127.0.0.1', port=8080):
        """Create a Uvicorn test server

        Args:
            app (FastAPI, optional): the FastAPI app. Defaults to main.app.
            host (str, optional): the host ip. Defaults to '127.0.0.1'.
            port (int, optional): the port. Defaults to PORT.
        """
        self._startup_done = asyncio.Event()
        super().__init__(config=uvicorn.Config(app, host=host, port=port))

    async def startup(self, sockets: Optional[List] = None) -> None:
        """Override uvicorn startup"""
        await super().startup(sockets=sockets)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def up(self) -> None:
        """Start up server asynchronously"""
        self._serve_task = asyncio.create_task(self.serve())
        await self._startup_done.wait()

    async def down(self) -> None:
        """Shut down server asynchronously"""
        self.should_exit = True
        await self._serve_task


@pytest.fixture
async def server():
    """Start server as test fixture and tear down after test"""

    nonebot.init()
    app: FastAPI = nonebot.get_asgi()
    nonebot.load_plugins('src/plugins')

    server = UvicornTestServer(app)
    await server.up()
    yield
    await server.down()


@pytest.mark.asyncio
def test_main(server):
    pass
