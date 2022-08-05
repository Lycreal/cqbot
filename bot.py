import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_plugins('src/plugins')
nonebot.load_plugin("nonebot_plugin_help")
nonebot.load_plugin("nonebot_plugin_manager")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
