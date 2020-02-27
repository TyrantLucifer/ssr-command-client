# The command client of Linux based Python3

在Linux下使用的一款ssr命令行客户端

# 特性
- 支持订阅链接解析
- 支持指定本地代理端口
- 支持节点测试ping值

# 个人配置修改

修改项目中`conf.py`中的`UBSCRIBE_URL`为自己的订阅链接

# 安装方式

```shell

git clone https://github.com/TyrantLucifer/ssr-commend-client.git
pip3 install -r requirement.txt

```

# 使用方法

```
python3 main.py [OPTIONS]

OPTIONS

-l --list "show ssr list" 展示ssr节点列表
-s --start "start ssr proxy" 启动ssr代理服务
-S --stop "stop ssr proxy" 停止ssr代理服务
-p --port port "assign local port" 指定本地代理端口
-c --config ssr_node_id "generate config json file" 生成指定节点json文件
-u --update "update ssr list" 更新ssr节点列表

```

# 未来计划

- [ ] 支持多订阅链接解析
- [ ] 支持自动选择速度最优节点
- [ ] 支持自动生成PAC代理文件
- [ ] 支持一键关闭、开启系统PAC网络代理(针对于Ubuntu 18.04)
- [ ] 支持指定ssr链接启动服务
- [ ] 支持命令行解析ssr链接信息

# Tips

如果有好的建议，欢迎发邮件给我，或者关注下方我的个人微信公众号在后台留言

- Email:Tyrantlucifer@linuxstudy.cn
- Blog:www.linuxstudy.cn
- Personal Wechat
![](https://cdn.jsdelivr.net/gh/TyrantLucifer/MyImageRepository/img/wechat.jpg)


