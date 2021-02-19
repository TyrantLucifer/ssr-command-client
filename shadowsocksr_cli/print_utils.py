"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: print_utils.py
@time: 2021/2/18 19:28
@desc: 提供打印功能工具类
"""

import qrcode
from prettytable import PrettyTable
from colorama import init, Fore


class DrawShadowsocksrListTable(object):
    """打印shadowsocksr节点信息表格工具类

    可生成终端shadowsocksr节点信息表格string

    属性:
        None
    """

    def __init__(self):
        self.table = []
        header = [
            "id",
            "name",
            "delay(ms)",
            "connect",
            "server",
            "port",
            "method"
        ]
        self.x = PrettyTable(header)
        self.x.reversesort = True

    def append(self, **kwargs):
        if kwargs:
            content = [
                kwargs['id'],
                kwargs['name'],
                kwargs['delay'],
                kwargs['connect'],
                kwargs['server'],
                kwargs['port'],
                kwargs['method']
            ]
            self.x.add_row(content)

    def str(self):
        return str(self.x)

    def print(self):
        print(self.str())


class DrawShadowsocksrSpeedTable(object):
    """打印shadowsocksr测速信息表格工具类

    可生成终端shadowsocksr节点测速信息表格string

    属性:
        None
    """

    def __init__(self):
        self.table = []
        header = [
            "id",
            "name",
            "download(MB/s)",
            "upload(MB/s)",
            "server",
            "port",
            "method"
        ]
        self.x = PrettyTable(header)
        self.x.reversesort = True

    def append(self, **kwargs):
        if kwargs:
            content = [
                kwargs['id'],
                kwargs['name'],
                kwargs['download'],
                kwargs['upload'],
                kwargs['server'],
                kwargs['port'],
                kwargs['method'],
            ]
            self.x.add_row(content)

    def str(self):
        return str(self.x)

    def print(self):
        print(self.str())


class Colored(object):
    """生成不同颜色字体工具类

    通过传入颜色，返回对应终端的颜色格式化字体

    属性:
        color: 支持颜色集合
    """

    def __init__(self):
        init(autoreset=False)
        self.color = (
            'red',
            'green',
            'yellow',
            'white',
            'blue'
        )

    @staticmethod
    def red(s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    @staticmethod
    def green(s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    @staticmethod
    def yellow(s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    @staticmethod
    def white(s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    @staticmethod
    def blue(s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

    def print(self, text, color):
        if color == 'red':
            print(self.red(text))
        if color == 'green':
            print(self.green(text))
        if color == 'yellow':
            print(self.yellow(text))
        if color == 'white':
            print(self.white(text))
        if color == 'blue':
            print(self.blue(text))


class PrintQrcode(object):
    """打印二维码工具类

    可使用该工具类的静态方法通过字符串打印任意的二维码

    属性:
        None
    """

    def __init__(self):
        pass

    @staticmethod
    def print_qrcode(string):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=1,
        )
        qr.add_data(string)
        qr.make(fit=True)
        qr.print_ascii(tty=True, invert=True)
