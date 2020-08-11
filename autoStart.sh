##########################################################################
# File Name: autoStart.sh
# Author: TyrantLucifer
# mail: TyrantLucifer@linuxstudy.cn
# Created Time: Wed 03 Jun 2020 09:49:37 PM CST
##########################################################################
#!/bin/bash

# 初始化环境变量
export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

# 获取当前登陆用户
user=`whoami`

# 获取当前目录
directory=`pwd`

sudo echo "
[Unit]
Description=ssr service
After=network.target syslog.target
Wants=network.target

[Service]
Type=forking
User=${user}
Group=${user}
ExecStart=/usr/bin/python3 ${directory}/main.py -s
ExecStop=/usr/bin/python3 ${directory}/main.py -S

[Install]
WantedBy=default.target
" > /lib/systemd/system/ssr.service

sudo systemctl enable ssr
echo "setting ssr auto start success"
