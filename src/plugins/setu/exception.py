from httpx import TimeoutException, NetworkError, TransportError


class ImageLoadError(Exception):
    pass


class ImageSizeError(ImageLoadError):
    pass


__all__ = [
    "TimeoutException", "NetworkError", "TransportError",
    "ImageSizeError", "ImageLoadError"
]
