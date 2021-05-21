import nonebot
from nonebot.adapters.cqhttp import Bot

import pytest
from starlette.testclient import TestClient, WebSocketTestSession

from .message import self_id


@pytest.fixture(scope="package")
def websocket() -> WebSocketTestSession:
    nonebot.init()
    driver = nonebot.get_driver()
    driver.register_adapter("cqhttp", Bot)
    nonebot.load_plugins('src/plugins')
    app = nonebot.get_asgi()

    client = TestClient(app)

    with client.websocket_connect(
            url='/cqhttp/ws',
            headers={'X-Self-ID': str(self_id)}
    ) as websocket:  # type: WebSocketTestSession
        yield websocket
