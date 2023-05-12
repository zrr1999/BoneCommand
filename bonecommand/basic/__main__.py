#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/2/3 23:41
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import cmd
import sys
from bonecommand import SingleCommand, MultiCommand
from bonecommand.utils import user_path


def install():
    if sys.platform == "darwin":
        pm = "brew"
    elif sys.platform == "linux":
        pm = "apt-get"
    else:
        pm = ""
    cmd = SingleCommand("apt-get")


def get_pip():
    cmd = MultiCommand(
        [
            "sudo apt install python3-distutils",
            "curl https://bootstrap.pypa.io/get-pip.py -o .temp.get-pip.py",
            f"{sys.executable} .temp.get-pip.py",
        ]
    )
    cmd.run()
