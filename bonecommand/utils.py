#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/21 23:36
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import sys
import os

user_path = os.path.expanduser("~")


def enable_working_path(working_path: str):
    sys.path.append(working_path)
    os.chdir(working_path)
