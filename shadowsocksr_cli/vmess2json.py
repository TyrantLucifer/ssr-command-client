import sys
import json
import base64
import pprint
import urllib.request
import urllib.parse

TPL = dict()

TPL["CLIENT"] = """
{
  "log": {
    "access": "",
    "error": "",
    "loglevel": "error"
  },
  "inbounds": [
  {
      "tag": "socks",
      "port": 1080,
      "listen": "127.0.0.1",
      "protocol": "socks",
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls"
        ]
      },
      "settings": {
        "auth": "noauth",
        "udp": true,
        "allowTransparent": false
      }
    },
    {
      "tag": "http",
      "port": 1081,
      "listen": "127.0.0.1",
      "protocol": "http",
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls"
        ]
      },
      "settings": {
        "udp": false,
        "allowTransparent": false
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "vmess",
      "settings": {
        "vnext": [
          {
            "address": "host.host",
            "port": 1234,
            "users": [
              {
                "email": "user@v2ray.com",
                "id": "",
                "alterId": 0,
                "security": "auto"
              }
            ]
          }
        ]
      },
      "streamSettings": {
        "network": "tcp"
      },
      "mux": {
        "enabled": true
      },
      "tag": "proxy"
    },
    {
      "protocol": "freedom",
      "tag": "direct",
      "settings": {
        "domainStrategy": "UseIP"
      }
    }
  ],
  "dns": {
    "servers": [
      "1.0.0.1",
      "8.8.8.8",
      "localhost"
    ]
  },
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {
        "type": "field",
        "ip": [
          "geoip:private",
          "geoip:cn"
        ],
        "outboundTag": "direct"
      },
      {
        "type": "field",
        "domain": [
          "geosite:cn"
        ],
        "outboundTag": "direct"
      }
    ]
  }
}
"""

# tcpSettings
TPL["http"] = """
{
    "header": {
        "type": "http",
        "request": {
            "version": "1.1",
            "method": "GET",
            "path": [
                "/"
            ],
            "headers": {
                "Host": [
                    "www.cloudflare.com",
                    "www.amazon.com"
                ],
                "User-Agent": [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
                ],
                "Accept": [
                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
                ],
                "Accept-language": [
                    "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"
                ],
                "Accept-Encoding": [
                    "gzip, deflate, br"
                ],
                "Cache-Control": [
                    "no-cache"
                ],
                "Pragma": "no-cache"
            }
        }
    }
}
"""

# kcpSettings
TPL["kcp"] = """
{
    "mtu": 1350,
    "tti": 50,
    "uplinkCapacity": 12,
    "downlinkCapacity": 100,
    "congestion": false,
    "readBufferSize": 2,
    "writeBufferSize": 2,
    "header": {
        "type": "wechat-video"
    }
}
"""

# wsSettings
TPL["ws"] = """
{
    "connectionReuse": true,
    "path": "/path",
    "headers": {
        "Host": "host.host.host"
    }
}
"""

# httpSettings
TPL["h2"] = """
{
    "host": [
        "host.com"
    ],
    "path": "/host"
}
"""

TPL["quic"] = """
{
  "security": "none",
  "key": "",
  "header": {
    "type": "none"
  }
}
"""

TPL["in_socks"] = """
{
    "tag":"socks-in",
    "port": 10808,
    "listen": "::",
    "protocol": "socks",
    "settings": {
        "auth": "noauth",
        "udp": true,
        "ip": "127.0.0.1"
    }
}
"""

TPL["in_http"] = """
{
    "tag":"http-in",
    "port": 8123,
    "listen": "::",
    "protocol": "http"
}
"""

TPL["in_mt"] = """
{
    "tag": "mt-in",
    "port": 6666,
    "protocol": "mtproto",
    "settings": {
        "users": [
            {
                "secret": ""
            }
        ]
    }
}
"""

TPL["out_mt"] = """
{
    "tag": "mt-out",
    "protocol": "mtproto",
    "proxySettings": {
        "tag": "proxy"
    }
}
"""

TPL["in_dns"] = """
{
  "port": 53,
  "tag": "dns-in",
  "protocol": "dokodemo-door",
  "settings": {
    "address": "1.1.1.1",
    "port": 53,
    "network": "tcp,udp"
  }
}
"""

TPL["conf_dns"] = """
{
    "hosts": {
        "geosite:category-ads": "127.0.0.1",
        "domain:googleapis.cn": "googleapis.com"
    },
    "servers": [
        "1.0.0.1",
        {
            "address": "1.2.4.8",
            "domains": [
                "geosite:cn"
            ],
            "port": 53
        }
    ]
}
"""

TPL["in_tproxy"] = """
{
    "tag":"tproxy-in",
    "port": 1080,
    "protocol": "dokodemo-door",
    "settings": {
        "network": "tcp,udp",
        "followRedirect": true
    },
    "streamSettings": {
        "sockopt": {
            "tproxy":"tproxy"
        }
    },
    "sniffing": {
        "enabled": true,
        "destOverride": [
            "http",
            "tls"
        ]
    }
}
"""

TPL["in_api"] = """
{
    "tag": "api",
    "port": 10085,
    "listen": "127.0.0.1",
    "protocol": "dokodemo-door",
    "settings": {
        "address": "127.0.0.1"
    }
}
"""

TPL["out_ss"] = """
{
    "email": "user@ss",
    "address": "",
    "method": "",
    "ota": false,
    "password": "",
    "port": 0
}
"""

V2RAY_SCHEMA = "vmess://"
SS_SCHEMA = "ss://"


def parse_link(link):
    if link.startswith(SS_SCHEMA):
        return parse_ss(link)
    elif link.startswith(V2RAY_SCHEMA):
        return parse_vemss(link)
    else:
        print("ERROR: This script supports only vmess://(N/NG) and ss:// links")
        return None


def parse_ss(ss_link):
    res_obj = {
        "v": "2",
        "ps": "",
        "add": "",
        "port": "",
        "id": "",
        "aid": "",
        "net": "shadowsocks",
        "type": "",
        "host": "",
        "path": "",
        "tls": ""
    }
    if ss_link.startswith(SS_SCHEMA):
        info = ss_link[len(SS_SCHEMA):]

        if info.rfind("#") > 0:
            info, _ps = info.split("#", 2)
            res_obj["ps"] = urllib.parse.unquote(_ps)

        if info.find("@") < 0:
            # old style link
            # paddings
            blen = len(info)
            if blen % 4 > 0:
                info += "=" * (4 - blen % 4)

            info = base64.b64decode(info).decode()

            atidx = info.rfind("@")
            method, password = info[:atidx].split(":", 2)
            addr, port = info[atidx + 1:].split(":", 2)
        else:
            atidx = info.rfind("@")
            addr, port = info[atidx + 1:].split(":", 2)

            info = info[:atidx]
            blen = len(info)
            if blen % 4 > 0:
                info += "=" * (4 - blen % 4)

            info = base64.b64decode(info).decode()
            method, password = info.split(":", 2)

        res_obj["add"] = addr
        res_obj["port"] = port
        res_obj["aid"] = method
        res_obj["id"] = password
        return res_obj


def parse_vemss(vmesslink):
    if vmesslink.startswith(V2RAY_SCHEMA):
        bs = vmesslink[len(V2RAY_SCHEMA):]
        # paddings
        blen = len(bs)
        if blen % 4 > 0:
            bs += "=" * (4 - blen % 4)

        vms = base64.b64decode(bs).decode()
        return json.loads(vms)
    else:
        raise Exception("vmess link invalid")


def load_TPL(stype):
    s = TPL[stype]
    return json.loads(s)


def fill_basic(_c, _v):
    _outbound = _c["outbounds"][0]
    _vnext = _outbound["settings"]["vnext"][0]

    _vnext["address"] = _v["add"]
    _vnext["port"] = int(_v["port"])
    _vnext["users"][0]["id"] = _v["id"]
    _vnext["users"][0]["alterId"] = int(_v["aid"])

    _outbound["streamSettings"]["network"] = _v["net"]

    if _v["tls"] == "tls":
        _outbound["streamSettings"]["security"] = "tls"
        _outbound["streamSettings"]["tlsSettings"] = {"allowInsecure": True}
        if _v["host"] != "":
            _outbound["streamSettings"]["tlsSettings"]["serverName"] = _v["host"]

    return _c


def fill_shadowsocks(_c, _v):
    _ss = load_TPL("out_ss")
    _ss["email"] = _v["ps"] + "@ss"
    _ss["address"] = _v["add"]
    _ss["port"] = int(_v["port"])
    _ss["method"] = _v["aid"]
    _ss["password"] = _v["id"]

    _outbound = _c["outbounds"][0]
    _outbound["protocol"] = "shadowsocks"
    _outbound["settings"]["servers"] = [_ss]

    del _outbound["settings"]["vnext"]
    del _outbound["streamSettings"]
    del _outbound["mux"]

    return _c


def fill_tcp_http(_c, _v):
    tcps = load_TPL("http")
    tcps["header"]["type"] = _v["type"]
    if _v["host"] != "":
        # multiple host
        tcps["header"]["request"]["headers"]["Host"] = _v["host"].split(",")

    if _v["path"] != "":
        tcps["header"]["request"]["path"] = [_v["path"]]

    _c["outbounds"][0]["streamSettings"]["tcpSettings"] = tcps
    return _c


def fill_kcp(_c, _v):
    kcps = load_TPL("kcp")
    kcps["header"]["type"] = _v["type"]
    _c["outbounds"][0]["streamSettings"]["kcpSettings"] = kcps
    return _c


def fill_ws(_c, _v):
    wss = load_TPL("ws")
    wss["path"] = _v["path"]
    wss["headers"]["Host"] = _v["host"]
    _c["outbounds"][0]["streamSettings"]["wsSettings"] = wss
    return _c


def fill_h2(_c, _v):
    h2s = load_TPL("h2")
    h2s["path"] = _v["path"]
    h2s["host"] = [_v["host"]]
    _c["outbounds"][0]["streamSettings"]["httpSettings"] = h2s
    return _c


def fill_quic(_c, _v):
    quics = load_TPL("quic")
    quics["header"]["type"] = _v["type"]
    quics["security"] = _v["host"]
    quics["key"] = _v["path"]
    _c["outbounds"][0]["streamSettings"]["quicSettings"] = quics
    return _c


def vmess2client(_t, _v):
    _net = _v["net"]
    _type = _v["type"]

    if _net == "shadowsocks":
        return fill_shadowsocks(_t, _v)

    _c = fill_basic(_t, _v)

    if _net == "kcp":
        return fill_kcp(_c, _v)
    elif _net == "ws":
        return fill_ws(_c, _v)
    elif _net == "h2":
        return fill_h2(_c, _v)
    elif _net == "quic":
        return fill_quic(_c, _v)
    elif _net == "tcp":
        if _type == "http":
            return fill_tcp_http(_c, _v)
        return _c
    else:
        pprint.pprint(_v)
        raise Exception("this link seem invalid to the script, please report to dev.")


def parse(v2ray_link):
    line = parse_link(v2ray_link)
    return vmess2client(load_TPL("CLIENT"), line)


if __name__ == "__main__":
    print(parse(sys.argv[1]))
