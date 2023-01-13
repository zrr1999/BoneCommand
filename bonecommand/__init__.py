#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/21 23:29
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from .command import CommandBase, MultiCommand, SingleCommand, ShellCommand

__version__ = "0.0.1"
all_commands = [
    "git",
    "pdf",
    "ssh",
]
