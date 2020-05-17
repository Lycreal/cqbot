QQ机器人-直播开播提醒
-------------
个人自用QQ机器人，主要用于在群聊中提醒直播开播，支持BiliBili，Youtube，网易CC。对于不同群聊分别保存配置。

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
# 首先保证酷Q能够正常运行
git clone https://github.com/Lycreal/qbot.git
cd qbot
# 修改docker-compose.yml中酷Q的路径和QQ号
docker-compose up -d
```

更多说明参考[Docker Compose官方文档](https://docs.docker.com/compose/reference/overview/)

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
直播开播提醒功能位于`plugins/group/monitor_notify`。此外还有一些其他自用插件，可自行移至`plugins/disabled`禁用。

### TODO
- ~~私聊开播提醒~~
- ~~在私聊中编辑群聊监控列表~~
- ~~一次添加/删除多个直播间监控~~
- ~~删除监控支持输入url~~
- ~~目前配置中储存的频道名称为所有群聊共用，将在后续版本分离~~

代码太乱了暂时不想继续开发了

## License
[MIT LICENSE](LICENSE)
