#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/21 23:29
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from .command import CommandBase  # noqa: F401
from .command import MultiCommand  # noqa: F401
from .command import SingleCommand  # noqa: F401
from .command import ShellCommand  # noqa: F401
from .command import ParallelCommand  # noqa: F401
from .command import SequenceCommand  # noqa: F401

__version__ = "0.0.2"
all_commands = [
    "git",
    "pdf",
    "ssh",
]
