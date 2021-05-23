# https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-local-per-directory-plugins

import nonebot
import pytest
from nonebot.adapters.cqhttp import Bot
from starlette.testclient import TestClient, WebSocketTestSession, Message

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
def websocket(client, monkeypatch) -> WebSocketTestSession:
    def mock_receive(self) -> Message:
        message = self._send_queue.get(timeout=30)
        if isinstance(message, BaseException):
            raise message
        return message

    monkeypatch.setattr(WebSocketTestSession, 'receive', mock_receive)

    self_id = NewNumber.self_id()
    with client.websocket_connect(url='/cqhttp/ws', headers={'X-Self-ID': str(self_id)}) as websocket:
        websocket.__setattr__('self_id', self_id)
        yield websocket
