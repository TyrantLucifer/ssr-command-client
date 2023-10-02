"""
Adapted from [Xiangsong Zeng](https://gist.github.com/zengxs)
Reference gist: proxy_socks2http.py https://gist.github.com/zengxs/dc6cb4dea4495ecaab7b44abb07a581f
"""
import asyncio
import logging
import re
from asyncio import StreamReader, StreamReaderProtocol, StreamWriter
from collections import namedtuple
from typing import Optional

import socks  # use pysocks

logging.basicConfig(level=logging.INFO)

HttpHeader = namedtuple(
    "HttpHeader", ["method", "url", "version", "connect_to", "is_connect"]
)


async def dial(client_conn, server_conn):
    async def io_copy(reader: StreamReader, writer: StreamWriter):
        while True:
            data = await reader.read(8192)
            if not data:
                break
            writer.write(data)
        writer.close()

    asyncio.ensure_future(io_copy(client_conn[0], server_conn[1]))
    asyncio.ensure_future(io_copy(server_conn[0], client_conn[1]))


async def open_socks5_connection(
    host: str,
    port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    socks_host: str = "localhost",
    socks_port: int = 1080,
    limit=2**16,
    loop=None
):
    s = socks.socksocket()
    s.set_proxy(
        socks.SOCKS5,
        addr=socks_host,
        port=socks_port,
        username=username,
        password=password,
    )
    s.connect((host, port))

    if not loop:
        loop = asyncio.get_event_loop()

    reader = StreamReader(limit=limit, loop=loop)
    protocol = StreamReaderProtocol(reader, loop=loop)
    transport, _ = await loop.create_connection(lambda: protocol, sock=s)
    writer = StreamWriter(transport, protocol, reader, loop)
    return reader, writer


async def read_until_end_of_http_header(reader: StreamReader) -> bytes:
    lines = []
    while True:
        line = await reader.readline()
        lines.append(line)
        if line == b"\r\n":
            break

    return b"".join(lines)


def parse_http_header(header: bytes) -> HttpHeader:
    lines = header.split(b"\r\n")
    fl = lines[0].decode()
    method, url, version = fl.split(" ", 2)

    if method.upper() == "CONNECT":
        host, port = url.split(":", 1)
        port = int(port)
    else:
        # find Host header line
        host_text = None
        for header_line in lines:
            hl = header_line.decode()
            if re.match(r"^host:", hl, re.IGNORECASE):
                host_text = re.sub(r"^host:\s*", "", hl, count=1, flags=re.IGNORECASE)
                break

        if not host_text:
            raise ValueError("No http host line")

        if ":" not in host_text:
            host = host_text
            port = 80
        else:
            host, port = host_text.split(":", 1)
            port = int(port)

    is_connect = method.upper() == "CONNECT"
    return HttpHeader(
        method=method,
        url=url,
        version=version,
        connect_to=(host, port),
        is_connect=is_connect,
    )


async def handle_connection(reader: StreamReader, writer: StreamWriter, socks_port=1080):
    try:
        http_header_bytes = await read_until_end_of_http_header(reader)
        http_header = parse_http_header(http_header_bytes)
    except (IOError, ValueError) as e:
        logging.error(e)
        writer.close()
        return

    server_conn = await open_socks5_connection(
        host=http_header.connect_to[0],
        port=http_header.connect_to[1],
        socks_host="localhost",
        socks_port=socks_port,
    )

    if http_header.is_connect:
        writer.write(b"HTTP/1.0 200 Connection Established\r\n\r\n")
    else:
        server_writer = server_conn[1]
        server_writer.write(http_header_bytes)

    # 建立双向连接
    asyncio.ensure_future(dial((reader, writer), server_conn))


def main():
    loop = asyncio.get_event_loop()
    server = asyncio.start_server(handle_connection, host="localhost", port=7890)
    try:
        server = loop.run_until_complete(server)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()


if __name__ == "__main__":
    main()
