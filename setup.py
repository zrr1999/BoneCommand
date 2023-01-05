#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/21 23:37
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
from setuptools import setup, find_packages
from command import __version__

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='UTF-8') as fh:
    requirements = fh.readlines()

setup(
    name="powercommand",
    version=__version__,
    keywords=["command", "shell"],
    description="一个用于提升效率的命令行工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/zrr1999/PowerCommand",
    author="六个骨头",
    author_email="2742392377@qq.com",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
    scripts=[]
)
