##########################################################################
# File Name: main.sh
# Author: TyrantLucifer
# mail: TyrantLucifer@linuxstudy.cn
# Created Time: Wed 03 Jun 2020 10:17:52 PM CST
##########################################################################
#!/bin/bash

# 初始化环境变量
export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

# 初始化颜色变量
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

print_menu(){
    clear
    echo -e "SSR Command Client一键管理脚本
---- TyrantLucifer | linuxstudy.cn ----
${yellow}1. ${plain} ${green}打印ssr节点列表${plain}
${yellow}2. ${plain} ${green}启动ssr代理服务${plain}
${yellow}3. ${plain} ${green}停止ssr代理服务${plain}
${yellow}4. ${plain} ${green}更换ssr节点${plain}
${yellow}5. ${plain} ${green}更新ssr节点列表${plain}
${yellow}6. ${plain} ${green}更换速度最快节点${plain}
${yellow}7. ${plain} ${green}重置ssr订阅链接${plain}
${yellow}8. ${plain} ${green}添加ssr订阅链接${plain}
${yellow}9. ${plain} ${green}移除ssr订阅链接${plain}
${yellow}10.${plain} ${green}显示ssr订阅链接${plain}
${yellow}11.${plain} ${green}解析ssr链接${plain}
${yellow}12.${plain} ${green}添加ssr节点${plain}
${yellow}13.${plain} ${green}重新检测节点状态${plain}
${yellow}14.${plain} ${green}设置系统代理模式为pac(只支持Ubuntu Desktop)${plain}
${yellow}15.${plain} ${green}设置系统代理模式为全局(只支持Ubuntu Desktop)${plain}
${yellow}16.${plain} ${green}关闭系统代理(只支持Ubuntu Desktop)${plain}
${yellow}17.${plain} ${green}设置开机自启${plain}
${yellow}18.${plain} ${green}更新ssr-command-client${plain}
"
}

list_ssr(){
    clear
    python3 main.py -l
}

start_ssr(){
    python3 main.py -s
}

stop_ssr(){
    python3 main.py -S
}

change_ssr_node(){
    clear
    list_ssr
    stty erase '^H'
    stty erase '^?'
    echo "请输入你要设置的节点id:" 
    read id
    echo -e "你输入的节点id为:${green} ${id} ${plain}"
    python3 main.py -c ${id}
}

update_ssr_list(){
    clear
    sudo python3 main.py -u
    clear
    list_ssr
}

select_fast_node(){
    python3 main.py --fast-node
}

list_subcribe_url(){
    clear
    echo "当前订阅链接如下:"
    python3 main.py --list-url
}

reset_ssr_subcribe_url(){
    clear
    list_subcribe_url
    stty erase '^H'
    stty erase '^?'
    echo "请输入你要重置的ssr订阅链接:"
    read ssr_subcribe_url
    echo -e "你输入的ssr订阅链接为:${green} ${ssr_subcribe_url} ${plain}"
    python3 main.py --setting-url ${ssr_subcribe_url}
}

add_ssr_subcribe_url(){
    clear
    list_subcribe_url
    stty erase '^H'
    stty erase '^?'
    echo "请设置你要添加的ssr订阅链接:"
    read ssr_subcribe_url
    echo -e "你输入的ssr订阅链接为:${green} ${ssr_subcribe_url} ${plain}"
    python3 main.py --add-url ${ssr_subcribe_url}
}

remove_ssr_subcribe_url(){
    clear
    list_subcribe_url
    stty erase '^H'
    stty erase '^?'
    echo "请设置你要移除的ssr订阅链接:"
    read ssr_subcribe_url
    echo -e "你输入的ssr订阅链接为:${green} ${ssr_subcribe_url} ${plain}"
    python3 main.py --remove-url ${ssr_subcribe_url}
}

parse_ssr_url(){
    clear
    stty erase '^H'
    stty erase '^?'
    echo "请输入你要解析的ssr链接(ssr://xxxxxxxx):" 
    read ssr_url
    echo -e "你输入的ssr链接为:${green} ${ssr_url} ${plain}"
    python3 main.py --parse-url ${ssr_url}
}

add_ssr_node(){
    clear 
    stty erase '^H'
    stty erase '^?'
    echo "请输入你要添加的ssr链接(ssr://xxxxxxxx):" 
    read ssr_url
    echo -e "你输入的ssr链接为:${green} ${ssr_url} ${plain}"
    python3 main.py --add-ssr ${ssr_url}
}

test_ssr_node(){
    clear
    list_ssr
    stty erase '^H'
    stty erase '^?'
    echo "请输入你要测试的节点id:" 
    read id
    echo -e "你输入的节点id为:${green} ${id} ${plain}"
    sudo python3 main.py --test-again ${id}
}

setting_global_proxy(){
    python3 main.py --setting_global_proxy
}

setting_pac_proxy(){
    python3 main.py --setting_pac_proxy
}

close_system_proxy(){
    python3 main.py --close_system_proxy
}

setting_auto_start(){
    python3 main.py --setting_auto_start
}

update_ssr_command_client(){
    git pull
    pip3 install -r requirement.txt
}
print_menu

echo && read -e -p "请输入数字 [1-18]：" num
case "$num" in
    1)
        list_ssr
        ;;
    2)
        start_ssr
        ;;
    3)
        stop_ssr
        ;;
    4)
        change_ssr_node
        ;;
    5)
        update_ssr_list
        ;;
    6)
        select_fast_node
        ;;
    7)
        reset_ssr_subcribe_url
        ;;
    8)
        add_ssr_subcribe_url
        ;;
    9)
        remove_ssr_subcribe_url
        ;;
    10)
        list_subcribe_url
        ;;
    11)
        parse_ssr_url
        ;;
    12)
        add_ssr_node
        ;;
    13)
        test_ssr_node
        ;;
    14)
        setting_global_proxy
        ;;
    15)
        setting_pac_proxy
        ;;
    16)
        close_system_proxy
        ;;
    17)
        setting_auto_start
        ;;
    18)
        update_ssr_command_client
        ;;
esac


