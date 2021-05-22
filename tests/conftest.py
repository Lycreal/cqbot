# https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-local-per-directory-plugins

import nonebot
from nonebot.adapters.cqhttp import Bot

import pytest
from starlette.testclient import TestClient, WebSocketTestSession

from .message import NewNumber


@pytest.fixture(scope="session")
def client():
    nonebot.init()
    driver = nonebot.get_driver()
    driver.register_adapter("cqhttp", Bot)
    nonebot.load_plugins('src/plugins')
    app = nonebot.get_asgi()

    client = TestClient(app)
    return client


@pytest.fixture(scope="function")
def websocket(client) -> WebSocketTestSession:
    self_id = NewNumber.self_id()
    with client.websocket_connect(
            url='/cqhttp/ws',
            headers={'X-Self-ID': str(self_id)}
    ) as websocket:  # type: WebSocketTestSession
        websocket.__setattr__('self_id', self_id)
        yield websocket
