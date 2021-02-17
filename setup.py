from setuptools import setup, find_packages

setup(
    name="ssr-command-client",
    version="2.1.0",
    author="tyrantlucifer",
    author_email="tyrantlucifer@gmail.com",
    description="The command client of shadowsocksR",
    url="https://github.com/tyrantlucifer/ssr-command-client", 
    packages=[
        "ssr_cli",
        "ssr_cli.functions",
        "ssr_cli.logger",
        "ssr_cli.shadowsocks",
        "ssr_cli.shadowsocks.crypto",
        "ssr_cli.shadowsocks.obfsplugin",
        "ssr_cli.speedtest",
        "ssr_cli.utils",
    ],
    entry_points={
        'console_scripts': [
            'ssr-cli = ssr_cli.main:main'
        ]
    },
    install_requires=[
        "requests",
        "prettytable",
        "PySocks",
        "qrcode",
        "pyyaml",
        "colorama"
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers',
    ],
)
