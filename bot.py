import nonebot
from nonebot.adapters.cqhttp import Bot

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot)

nonebot.load_plugin("src.plugins.pic_searcher")
nonebot.load_plugin("src.plugins.cats")
nonebot.load_plugin("src.plugins.setu")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
