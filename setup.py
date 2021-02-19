from setuptools import setup

setup(
    name="shadowsocksr-cli",
    version="2.1.0",
    author="tyrantlucifer",
    author_email="tyrantlucifer@gmail.com",
    description="The command client of shadowsocksr",
    url="https://github.com/tyrantlucifer/ssr-command-client", 
    packages=[
        "shadowsocksr_cli",
        "shadowsocksr_cli.shadowsocks",
        "shadowsocksr_cli.shadowsocks.crypto",
        "shadowsocksr_cli.shadowsocks.obfsplugin"
    ],
    entry_points={
        'console_scripts': [
            'shadowsocksr-cli = shadowsocksr_cli.main:main'
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers',
    ],
)
