#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/7 20:36
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import typer
from bonecommand import SingleCommand

app = typer.Typer()


@app.command()
def accelerate_github(mode: str = "ssh"):
    assert mode == "ssh"
    cmd = SingleCommand(
        "git config --global url.'git@github.com:'.insteadOf 'https://github.com/'"
    )
    cmd.run()


if __name__ == "__main__":
    app()
