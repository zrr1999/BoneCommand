#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 16:41
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import typer
import psutil
from rich.console import Console
from bonecommand.utils import user_path

app = typer.Typer(add_completion=False)


@app.command()
def install(install_completion: bool = False):
    console = Console()
    supported_shell = ["zsh", "bash"]
    shell = psutil.Process().parent().name()
    if shell not in supported_shell:
        console.print(
            "You should install [bold cyan]BoneCommand[/bold cyan] cli in shell(zsh/bash).",
            style="bold red",
        )

    with open(f"{user_path}/.{shell}rc", mode="r") as f:
        print(f"{user_path}/.{shell}rc")
        print(f.readlines()[-1])
    with open(f"{user_path}/.{shell}rc", mode="a") as f:
        # print(f.readlines()[-1])
        f.write("\ntest\n")


@app.command()
def show_command():
    print(
        "\n".join(
            [
                "git",
                "pdf",
                "ssh",
            ]
        )
    )


if __name__ == "__main__":
    app()
