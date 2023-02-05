# DLimiter
用于下载器平衡PT上传和外网视频播放的限速器

## 用途

在我们使用 qBittorrent 、Transmission 进行 PT、BT 保种的时候，小水管上传很容易被跑满。
这时候如果用户想在外网访问家里的 NAS 使用 Emby 等软件播放视频的时候，就会异常的卡顿。

因此，此小工具利用 Emby Webhooks功能，当接收到外网设备的播放Webhooks时，对下载器进行限速；当接受到外网设备的播放结束Webhooks时，对下载器取消限速。

业余摸鱼工具(~~屎山~~)，如有意见，建议issue或直接pr。

## 使用方法

首先将本项目clone到本地。复制conf文件夹里的`config_example.toml`，重命名为`config.toml`，并配置相关信息，放在本项目文件夹。然后执行：

### docker-compose

```bash
docker-compose up -d
```

### docker-cli

```bash
docker run -d \
    --name=dlimiter \
    -p 8088:8088 \
    -e DLIMITER_CN_UPDATE=true \
    -e DLIMITER_AUTO_UPDATE=true \
    -e DLIMITER_PORT=8088 \
    -e TZ=Asia/Shanghai \
    -v ${PWD}/conf:/app/conf \
    --hostname=dlimiter \
    --restart=always \
    steve0x2a/dlimiter:latest
```

确保程序正确运行后，打开播放器的后台页面，添加 webhooks 。如 Emby 设置如下：
![](https://vip2.loli.io/2023/02/04/coeBCiRsXtkhFVI.png)

## Webhooks

### Emby
- URI: `/player/emby`
- 事件: 播放事件


## 配置文件解析

首先是`exclude_ip`

```toml
[limiter]
exclude_ip = ["192.168.2.1","10.144.1.0/24"]
```

当接收到 Webhooks 时，会先判断是否为外网ip。

但由于家宽很多设备都是利用路由器端口转发出去的，因此在emby看来，播放设备的ip地址为路由器自身的LAN地址，因此，我们要特殊处理该地址。

另外，我们经常会使用类似 Zerotier 等虚拟内网设备访问 NAS ，因此虚拟内网的网段也许要被排除。

然后是`emby`设置：

```toml
[emby]
enable = true
url="http://127.0.0.1:8096"
api_key="xxx"
```
这里没什么好说，配置url和apikey即可

最后是`downloader`设置：

目前支持两种下载器：`qBittorrent` 及 `Transmission` 。根据样例配置文件即可配置多个下载器。

`use_alt_speed_limits`选项是考虑到部分用户会使用到qb的`备用速度`和tr的时段控制功能，如果使用了这两个功能，设为`true`即可。

另外，由于qb和tr不限制速度的设置不太一样，因此如果不想进行某项速度的限制，建议将速度限制改为较大的数值（作者偷懒\o/)


## TODO
- [ ] 支持其他播放器
- [ ] 支持更多限速方式不仅限于Webhooks