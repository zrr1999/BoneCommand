#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/7 16:26
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import typer
import pyperclip
import os
from command import SingleCommand, MultiCommand

app = typer.Typer()


@app.command()
def show_pub(copy: bool = False):
    user_path = os.path.expanduser('~')
    if not os.path.exists(f"{user_path}/.ssh/id_rsa.pub"):
        email = SingleCommand("git config user.email").get_output()
        cmd = MultiCommand([
            f"ssh-keygen -t rsa -C '{email}'",
            f"cat {user_path}/.ssh/id_rsa.pub"
        ])
    else:
        cmd = SingleCommand(f"cat {user_path}/.ssh/id_rsa.pub")
    out = cmd.get_output()
    print(out)
    if copy:
        pyperclip.copy(out)


if __name__ == '__main__':
    app()
