"""
@author: tyrantlucifer
@contact: tyrantlucifer@gmail.com
@blog: https://tyrantlucifer.com
@file: http_utils.py
@time: 2021/2/21 22:43
@desc: 提供http pac代理功能
"""

import atexit
import signal
import socket
import re
import requests
import threading
from shadowsocksr_cli.logger import *


class Daemon(object):
    """
    a generic daemon class.
    usage: subclass the Daemon class and override the run() method
    stderr  表示错误日志文件绝对路径, 收集启动过程中的错误日志
    verbose 表示将启动运行过程中的异常错误信息打印到终端,便于调试,建议非调试模式下关闭, 默认为1, 表示开启
    save_path 表示守护进程pid文件的绝对路径
    """

    def __init__(self, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=22,
                 verbose=1):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = save_path  # pid文件绝对路径
        self.home_dir = home_dir
        self.verbose = verbose  # 调试开关
        self.umask = umask
        self.daemon_alive = True

    '''
    编写守护进程的一般步骤步骤：
    （1）创建自己成并被init进程接管：在父进程中执行fork并exit退出；
    （2）创建新进程组和新会话：在子进程中调用setsid函数创建新的会话；
    （3）修改子进程的工作目录：在子进程中调用chdir函数，让根目录 ”/” 成为子进程的工作目录；
    （4）修改子进程umask：在子进程中调用umask函数，设置进程的umask为0；
    （5）在子进程中关闭任何不需要的文件描述符

    在子进程中再次fork一个进程，这个进程称为孙子进程，之后子进程退出
    重定向孙子进程的标准输入流、标准输出流、标准错误流到/dev/null
    那么最终的孙子进程就称为守护进程。
    '''

    def daemonize(self):
        try:
            '''
            进程调用fork函数时，操作系统会新建一个子进程，它本质上与父进程完全相同。子进程从父进程继承了多个值的拷贝，比如全局变量和环境变量。
            两个进程唯一的区别就是fork的返回值。child（子）进程接收返回值为0，而父进程接收子进程的pid作为返回值。
            调用fork函数后，两个进程并发执行同一个程序，首先执行的是调用了fork之后的下一行代码。父进程和子进程既并发执行，又相互独立。
            '''
            # 创建子进程，而后父进程退出
            # 为避免挂起控制终端将Daemon放入后台执行。方法是在进程中调用fork使父进程终止，让Daemon在子进程中后台执行。
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        # 创建新会话，子进程成为新会话的首进程（session leader）
        '''
        setsid()函数可以建立一个对话期。

        会话期(session)是一个或多个进程组的集合。
        如果，调用setsid的进程不是一个进程组的组长，此函数创建一个新的会话期。
        (1)此进程变成该对话期的首进程
        (2)此进程变成一个新进程组的组长进程。
        (3)此进程没有控制终端，如果在调用setsid前，该进程有控制终端，那么与该终端的联系被解除。 如果该进程是一个进程组的组长，此函数返回错误。
        (4)为了保证这一点，我们先调用fork()然后exit()，此时只有子进程在运行
        '''
        # 创建新的会话，子进程成为会话的首进程
        # 控制终端，登录会话和进程组通常是从父进程继承下来的。我们的目的就是要摆脱它们，使之不受它们的影响。方法是在创建子进程的基础上，调用setsid()使进程成为会话组长
        os.setsid()

        # 修改子进程的工作目录
        os.chdir(self.home_dir)

        '''
        由于umask会屏蔽权限，所以设定为0，这样可以避免读写文件时碰到权限问题。
        '''
        # 修改子进程umask为0
        os.umask(self.umask)

        '''
        现在，进程已经成为无终端的会话组长。但它可以重新申请打开一个控制终端。可以通过使进程不再成为会话组长来禁止进程重新打开控制终端：
        '''
        try:
            # 创建孙子进程，而后子进程退出
            # 新创建的孙子进程，不是会话组长
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        '''
        因为是守护进程，本身已经脱离了终端，那么标准输入流、标准输出流、标准错误流就没有什么意义了。
        所以都转向到/dev/null，就是都丢弃的意思。
        '''
        # 重定向孙子进程的标准输入流、标准输出流、标准错误流到/dev/null
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        if self.stderr:
            se = open(self.stderr, 'ab+', 0)
        else:
            se = so

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        def sig_handler(signum, frame):
            self.daemon_alive = False

        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)

        if self.verbose >= 1:
            print('daemon process started ...')

        atexit.register(self.del_pid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write('%s\n' % pid)

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def del_pid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self, *args, **kwargs):
        if self.verbose >= 1:
            logger.info("HTTP Server is starting...")
        # check for a pid file to see if the daemon already runs
        pid = self.get_pid()
        if pid:
            msg = 'pid file %s already exists, is it already running?\n'
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)
        # start the daemon
        self.daemonize()
        self.run(*args, **kwargs)

    def stop(self):
        if self.verbose >= 1:
            pass
        pid = self.get_pid()
        if not pid:
            msg = 'pid file [%s] does not exist. Not running?' % self.pidfile
            # sys.stderr.write(msg)
            logger.error(msg)
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            return
        # try to kill the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)
            if self.verbose >= 1:
                logger.info("HTTP Server is stopped...")

    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)

    def is_running(self):
        pid = self.get_pid()
        return pid and os.path.exists('/proc/%d' % pid)

    def run(self, *args, **kwargs):
        pass


class HTTPLocalServer(Daemon):

    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.', umask=22,
                 verbose=1):
        Daemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name
        self.server_socket = None

    def __init_http_server(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        self.server_socket.listen(128)

    def __deal_request(self, client_socket):
        request = client_socket.recv(1024).decode('unicode_escape')
        request_lines = request.splitlines()
        if len(request_lines) == 0 or re.match(r"[^/]+(/[^ ]*)", request_lines[0]) is None:
            return
        else:
            ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0]).group(1)
        if ret == "/":
            ret = "/index.html"
        index = ret.find('?')
        if index != -1:
            ret = ret[0:index]
        try:
            f = open(ret[1:], "rb")
        except FileNotFoundError:
            response_body = "file not found, 请输入正确的url"
            response_header = "HTTP/1.1 404 not found\r\n"
            response_header += "Content-Type: text/html; charset=utf-8\r\n"
            response_header += "\r\n"
            client_socket.send(response_header.encode('utf-8'))
            client_socket.send(response_body.encode("utf-8"))
        else:
            content = f.read()
            f.close()
            response_body = content
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html; charset=utf-8\r\n"
            response_header += "\r\n"
            client_socket.send(response_header.encode("utf-8") + response_body)

    def __serve_forever(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            self.__deal_request(client_socket)
            client_socket.close()

    def start_on_windows(self, *args, **kwargs):
        port = kwargs['http_port']
        self.__init_http_server(port)

        def handler(signum, frame):
            logger.info('received SIGQUIT, doing graceful shutting down..')
            GeneratePac.remove_pac()
            logger.info('HTTP Server stop...')
            exit(0)

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        logger.info("HTTP Server start on localhost:{0}...".format(port))
        t = threading.Thread(target=self.__serve_forever, args=())
        t.daemon = True
        t.start()
        while True:
            time.sleep(1)

    def run(self, *args, **kwargs):
        port = kwargs['http_port']
        self.__init_http_server(port)
        self.__serve_forever()
        logger.info("HTTP Server start on *:{0}".format(port))


class GeneratePac(object):

    def __init__(self):
        pass

    @staticmethod
    def __download_pac_template():
        logger.info("Start download pac template...")
        result = requests.get('https://tyrantlucifer.com/ssr/autoproxy.pac')
        result.encoding = 'utf-8'
        with open(init_config.pac_file, 'w', encoding='utf-8') as file:
            file.write(result.text)

    @staticmethod
    def generate_pac(address, port):
        if not os.path.exists(init_config.pac_file):
            GeneratePac.__download_pac_template()
        with open(init_config.pac_file, 'r', encoding='utf-8') as file:
            content = file.read()
        with open("autoproxy.pac", 'w', encoding='utf-8') as file:
            content = content.replace("address", address)
            content = content.replace("port", str(port))
            file.write(content)
        logger.info("Generate pac file successfully...")

    @staticmethod
    def remove_pac():
        os.remove("autoproxy.pac")
