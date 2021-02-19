"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: common.py
@time: 2021/2/18 19:09
@desc: 公共模块，为功能函数模块提供工厂代理
"""

from shadowsocksr_cli.print_utils import *
from shadowsocksr_cli.update_utils import *

# 初始化工具类print_utils.Colored
color = Colored()

# 初始化工具类print_utils.DrawShadowsocksrListTable
ssr_list_table = DrawShadowsocksrListTable()

# 初始化工具类print_utils.DrawShadowsocksrSpeedTable
ssr_speed_table = DrawShadowsocksrSpeedTable()

# 初始化工具类update_utils.UpdateShadowsocksr
update_shadowsocksr = UpdateShadowsocksr()