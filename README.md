# ssr-commend-client

---

基于Python3的ssr命令行客户端

---

# 特性
- 支持订阅链接解析
- 支持指定本地代理端口
- 支持节点测试ping值

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
- [  ] 支持多链接解析
- [  ] 支持自动选择速度最优节点
- [  ] 支持自动生成PAC代理文件
- [  ] 支持一键关闭、开启系统PAC网络代理




