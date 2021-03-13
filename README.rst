================
Shadowsocksr-cli
================

**Shadowsocksr-cli** is a client of Shadowsocksr based on python.

Features
--------

- Support Linux and Windows
- Support parse shadowsocksr information by shadowsocksr url
- Support parse shadowsocksr information by subscribe url
- Support test shadowsocksr connect status
- Support test shadowsocksr download and upload speed
- Support print shadowsocksr information by qrcode or json format
- Support generate clash fundamental config file

How to install
--------------

- Use source code

::

    git clone https://github.com/TyrantLucifer/ssr-command-client.git
    cd ssr-command-client
    python(python3) setup.py install

- Use pip

::

    pip(pip3) install shadowsocksr-cli

Usage
-----

::

    usage: shadowsocksr-cli [-h] [-l] [-p local_port] [-s ssr_id] [-S [ssr_id]] [-u] [-v]
                            [--generate-clash] [--display-json ssr_id] [--test-speed ssr_id]
                            [--fast-node] [--setting-url ssr_subscribe_url]
                            [--setting-address ssr_local_address] [--list-url]
                            [--add-url ssr_subscribe_url] [--remove-url ssr_subscribe_url]
                            [--list-address] [--parse-url ssr_url] [--add-ssr ssr_url]
                            [--test-again ssr_node_id] [--print-qrcode ssr_node_id]
                            [--http action[start stop status]] [--setting-global-proxy]
                            [--setting-pac-proxy] [--close-system-proxy] [--http-port port]

    The shadowsocksr command client based Python.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            show ssr list
  -p local_port, --port local_port
                        assign local proxy port,use with -s
  -s ssr_id, --start ssr_id
                        start ssr proxy
  -S ssr_id, --stop ssr_id
                        stop ssr proxy
  -u, --update          update ssr list
  -v, --version         display version
  --generate-clash      generate clash config yaml
  --display-json ssr_id
                        display ssr json info
  --test-speed ssr_id   test ssr nodes download and upload speed
  --fast-node           find most fast by delay and start ssr proxy
  --setting-url ssr_subscribe_url
                        setting ssr subscribe url
  --setting-address ssr_local_address
                        setting ssr local address
  --list-url            list ssr subscribe url
  --add-url ssr_subscribe_url
                        add ssr subscribe url
  --remove-url ssr_subscribe_url
                        remove ssr subscribe url
  --list-address        list ssr local address
  --parse-url ssr_url   pares ssr url
  --add-ssr ssr_url     add ssr node
  --test-again ssr_node_id
                        test ssr node again
  --print-qrcode ssr_node_id
                        print ssr node qrcode
  --setting-global-proxy
                        setting system global proxy,only support on
                        Ubuntu Desktop
  --setting-pac-proxy   setting system pac proxy,only support on Ubuntu
                        Desktop
  --close-system-proxy  close system proxy,only support on Ubuntu
                        Desktop
  --http action         open local http server, offer http pac proxy for system
  --http-port port      assign local http server port, default is 80


Documentation
-------------

You can find all the documentation in the
`Readme <https://github.com/TyrantLucifer/ssr-command-client>`__.

License
-------

MIT License

Copyright (c) 2021 **TyrantLucifer**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

