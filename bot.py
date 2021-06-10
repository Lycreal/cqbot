import nonebot
from nonebot.adapters.cqhttp import Bot

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot)

nonebot.load_plugins('src/plugins')
nonebot.load_plugin("nonebot_plugin_manager")
if driver.config.debug:
    nonebot.load_plugin("nonebot_plugin_test")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
