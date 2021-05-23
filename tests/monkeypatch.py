import json
import typing

from starlette.testclient import Message, WebSocketTestSession


class PatchWebSocketTestSession(WebSocketTestSession):
    DEFAULT_TIME_OUT = 30

    def receive(self, timeout: float = ...) -> Message:
        message = self._send_queue.get(timeout=timeout if timeout is not ... else self.DEFAULT_TIME_OUT)
        if isinstance(message, BaseException):
            raise message
        return message

    def receive_json(self, mode: str = "text", timeout: float = ...) -> typing.Any:
        assert mode in ["text", "binary"]
        message = self.receive(timeout=timeout)
        self._raise_on_close(message)
        if mode == "text":
            text = message["text"]
        else:
            text = message["bytes"].decode("utf-8")
        return json.loads(text)

    @classmethod
    def patch(cls):
        WebSocketTestSession.DEFAULT_TIME_OUT = cls.DEFAULT_TIME_OUT
        WebSocketTestSession.receive = cls.receive
        WebSocketTestSession.receive_json = cls.receive_json


PatchWebSocketTestSession.patch()
