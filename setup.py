import codecs
from setuptools import setup

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="shadowsocksr-cli",
    version="2.1.2",
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
