QQ机器人-直播开播提醒
-------------
开播提醒QQ机器人，基于 [酷Q](https://cqp.cc) 和 [nonebot](https://github.com/nonebot/nonebot) ，主要用于在群聊中提醒直播开播，支持BiliBili，Youtube，网易CC。对于不同群聊分别保存配置。

#### 效果展示
![](images/1.jpg)
### 特性
- 支持bilibili直播、youtube直播、cc直播
- 通过群聊命令编辑监控列表
- 自动获取频道名称，也可设置自定义名称
- 不同群聊分别储存监控列表
- 短时间内多条开播提醒进行合并

### 原理说明
总列表为每个群聊的监控列表的并集。对总列表中的直播间页面/API进行轮询，经判断为开播信号则发送至对应的监控了该直播间的群聊。

### 部署方法

```shell script
git clone https://github.com/Lycreal/qbot.git
cd qbot

# 修改docker-compose.yml中的QQ号
vim docker-compose.yml

docker-compose up -d
# 用浏览器访问 http://127.0.0.1:9000 登录酷Q （仅首次需要）
```

[cqhttp镜像文档](https://cqhttp.cc/docs/4.15/#/Docker)

[nonebot项目](https://github.com/nonebot/nonebot)

[Docker Compose命令行文档](https://docs.docker.com/compose/reference/overview/)

### 使用方法
命令以`.`开头，如`.help`、`.monitor`。具体帮助可部署成功后私聊bot进行查询。
```text
.monitor add <url> [name]
<url>  直播间地址
[name] 频道名,可省略并自动获取

.monitor add <type> <cid> [name]
<type> 频道类型,备选值:bili,you,cc
<cid>  频道id,对于bilibili指直播间号
[name] 频道名,可省略并自动获取

.monitor del <type> <cid>
<type> 频道类型
<cid>  频道id
注:可使用monitor list all查看频道id

.monitor list       查看频道列表及直播状态
.monitor list all   查看频道列表及频道id

.monitor help [add|del|list]    查看帮助
```

### 注意事项
直播提醒插件位于`plugins/group/monitor_notify`。此外还有一些自用插件，可移至`plugins/disabled`禁用。

### 开发计划

将 `live_monitor` 分离出来，作为独立的模块调用。


## License
[MIT LICENSE](LICENSE)
