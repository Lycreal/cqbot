from base64 import b64encode

from nonebot import Bot, on_message
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.rule import Rule
from nonebot.typing import T_State

from .datasource import CatPicture
from .exceptions import TimeoutException, NetworkError


def full_match(keyword: str) -> Rule:
    async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_plaintext().strip() == keyword:
            return True
        else:
            return False

    return Rule(_checker)


cats = on_message(full_match('猫猫'), state={'source': CatPicture})


@cats.handle()
async def cats_handler(bot: Bot, event: Event, state: T_State) -> None:
    try:
        image_bytes = await state['source'].get_image()
        file = f"base64://{b64encode(image_bytes).decode()}"
        await bot.send(event, MessageSegment.image(file))
    except TimeoutException:
        await bot.send(event, "请求超时", at_sender=True)
    except NetworkError:
        await bot.send(event, "网络错误", at_sender=True)
    except Exception as e:
        import traceback
        msg = '\n'.join(traceback.format_exception_only(type(e), e)).strip()
        await bot.send(event, msg, at_sender=True)
