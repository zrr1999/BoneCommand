#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/23 20:19
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from bonecommand.utils import enable_working_path


class Builder:
    def __init__(self, working_path: str = ".", build_dir="build"):
        enable_working_path(working_path)
        self.build_dir = build_dir

    def build(self):
        if rebuild:
            clean_command = [
                "rm *.plan",
                "rm so/plugins.so",
                "rm -rf build",
                "mkdir build",
            ]
            rich.print(clean_command)
            sp.run("\n".join(clean_command), shell=True)
