# The command client of Linux based Python3

在Linux下使用的一款ssr命令行客户端

## 特性

- 支持订阅链接解析
- 支持指定本地代理端口
- 支持节点测试ping值

## 个人配置修改

修改项目中`conf.py`中的`UBSCRIBE_URL`为自己的订阅链接

## 安装方式

```shell

git clone https://github.com/TyrantLucifer/ssr-commend-client.git
pip3 install -r requirement.txt

```

## 使用方法

```
python3 main.py [OPTIONS]

OPTIONS

-l --list "show ssr list" 展示ssr节点列表
-s --start "start ssr proxy" 启动ssr代理服务
-S --stop "stop ssr proxy" 停止ssr代理服务
-p --port port "assign local port" 指定本地代理端口
-c --config ssr_node_id "generate config json file" 生成指定节点json文件
-u --update "update ssr list" 更新ssr节点列表
-v --version "display version" 显示当前版本
```

## 效果展示

- 输出ssr链接节点列表 python3 main.py -l

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228002318.png)

- 更新ssr订阅链接 python3 main.py -u

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228002902.png)

- 生成ssr节点配置文件 python3 main.py -c `ssr_node_id`

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228003044.png)

- 指定本地代理端口并生成配置文件 python3 main.py -c `ssr_node_id` -p `local_port`

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228003139.png)

- 启动ssr代理 python3 main.py -s

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228003406.png)

- 停止ssr代理 python3 main.py -S

![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/20200228003529.png)

## 命令行设置代理方法

``` shell
export ALL_PROXY=socks5://127.0.0.1:1080 # 设置代理
unset ALL_PROXY # 关闭代理
curl https://ip.cn # 查看外网ip及ip归属地

```
如果想要方便的使用命令开关代理，可以将以下内容加入到自己的shell环境文件中：
``` shell
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1080"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl https://ip.cn"

```
这样下面这几个命令就会有以下功能：

`setproxy` 开启代理
`unsetproxy` 关闭代理
`ip` 查看ip归属地

## 未来计划

- [ ] 支持多订阅链接解析
- [ ] 支持自动选择速度最优节点
- [ ] 支持自动生成PAC代理文件
- [ ] 支持一键关闭、开启系统PAC网络代理(针对于Ubuntu 18.04)
- [ ] 支持指定ssr链接启动服务
- [ ] 支持命令行解析ssr链接信息

## Tips

如果有好的建议，欢迎发邮件给我，或者关注下方我的个人微信公众号在后台留言

- Email:Tyrantlucifer@linuxstudy.cn
- Blog:www.linuxstudy.cn
- Personal Wechat

![我的微信公众号](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat.jpg)


