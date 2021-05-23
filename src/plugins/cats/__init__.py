from nonebot import Bot, on_command
from nonebot.adapters.cqhttp import Event, MessageSegment
from nonebot.typing import T_State

from base64 import b64encode
from .exceptions import TimeoutException, NetworkError
from .datasource import CatPicture

cats = on_command('猫猫', state={'source': CatPicture})


@cats.handle()
async def cats_handler(bot: Bot, event: Event, state: T_State) -> None:
    try:
        image_bytes = await state['source'].get_image()
        file = f"base64://{b64encode(image_bytes).decode()}"
        await bot.send(event, MessageSegment.image(file), at_sender=True)
    except TimeoutException:
        await bot.send(event, "请求超时", at_sender=True)
    except NetworkError:
        await bot.send(event, "网络错误", at_sender=True)
    except Exception as e:
        import traceback
        msg = '\n'.join(traceback.format_exception_only(type(e), e)).strip()
        await bot.send(event, msg, at_sender=True)
