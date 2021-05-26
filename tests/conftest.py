# https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-local-per-directory-plugins
import os

import pytest
from starlette.testclient import TestClient, WebSocketTestSession, Message

from .message import NewNumber

os.environ['COMMAND_START'] = '["/", ""]'
os.environ['SUPERUSERS'] = "[222222]"
os.environ['moderatecontent_apikey'] = 'abc'


@pytest.fixture(scope="session")
def client():
    from bot import app
    client = TestClient(app)
    return client


@pytest.fixture(scope="function")
def websocket(client, monkeypatch) -> WebSocketTestSession:
    def mock_receive(self) -> Message:
        message = self._send_queue.get(timeout=20)
        if isinstance(message, BaseException):
            raise message
        return message

    monkeypatch.setattr(WebSocketTestSession, 'receive', mock_receive)

    self_id = NewNumber.self_id()
    with client.websocket_connect(url='/cqhttp/ws', headers={'X-Self-ID': str(self_id)}) as websocket:
        websocket.__setattr__('self_id', self_id)
        yield websocket
